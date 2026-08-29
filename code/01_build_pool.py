# Part of the Roman Urdu indicator resource pipeline. Paths are relative to the source datasets (RUHSOLD, RU-HSD-30K).
import pandas as pd, re, hashlib

# ---------- Load RUHSOLD (coarse task_1 + fine task_2 merged on text) ----------
def load_tsv(p):
    return pd.read_csv(p, sep='\t', header=None, names=['text','label'], quoting=3,
                       encoding='utf-8', on_bad_lines='skip').dropna()

coarse = pd.concat([load_tsv(f'RUHSOLD/task_1_{s}.tsv') for s in ['train','validation','test']])
fine   = pd.concat([load_tsv(f'RUHSOLD/task_2_{s}.tsv') for s in ['train','validation','test']])
coarse_map={0:'Abusive/Offensive',1:'Normal'}
fine_map={0:'Abusive/Offensive',1:'Normal',2:'Religious Hate',3:'Sexism',4:'Profane/Untargeted'}
coarse['text']=coarse['text'].astype(str).str.strip()
fine['text']=fine['text'].astype(str).str.strip()
coarse=coarse.drop_duplicates('text'); fine=fine.drop_duplicates('text')
ru=coarse.merge(fine, on='text', how='left', suffixes=('_c','_f'))
ru['orig_label']=ru['label_c'].map(coarse_map)
ru['fine_label']=ru['label_f'].map(fine_map)
ru=ru[['text','orig_label','fine_label']]; ru['source']='RUHSOLD'

# ---------- Load RU-HSD-30K ----------
r30=pd.read_csv('RUHSD30K/final 30,000 dataset_romanurdu.csv', encoding='latin-1',
                on_bad_lines='skip', engine='python')
r30=r30.rename(columns={'tweets':'text','label':'lab'})
r30['text']=r30['text'].astype(str).str.strip()
r30['orig_label']=r30['lab'].map({'H':'Hate/Offensive','N':'Normal'})
r30['fine_label']=None; r30['source']='RU-HSD-30K'
r30=r30[['text','orig_label','fine_label','source']]

pool=pd.concat([ru, r30], ignore_index=True)
# basic clean + dedupe on normalized text
def norm(t):
    t=re.sub(r'http\S+','',str(t)); t=re.sub(r'\s+',' ',t).strip().lower(); return t
pool['norm']=pool['text'].map(norm)
pool=pool[pool['norm'].str.len()>=8]                 # drop ultra-short
pool=pool.drop_duplicates('norm').reset_index(drop=True)
pool['tweet_id']=pool['norm'].map(lambda s: 'ru'+hashlib.md5(s.encode()).hexdigest()[:10])

# ---------- Relevance filter: keyword clusters aligned to the 6 indicators ----------
clusters={
 'grievance':['zulm','zulam','naiensaf','na insaf','nainsafi','mazloom','mehroom','dabaya','dabaa','loot','looto','corrupt','mehngai','mehngaai','berozgar','be rozgar','ghareeb','ghurbat','haq','haqooq','zulmat'],
 'ingroup_outgroup':['qaum','ummat','ghaddar','gaddar','ghadaar','dushman','deshdrohi','kaafir','kafir','yahudi','agent','lifafa','ghair','namak haram','bika','bikay'],
 'dehumanization':['keeray','keeda','kutta','kuttay','kutte','kuttey','jaanwar','janwar','haiwan','gandagi','naapak','napak','zaleel','zillat','cancer','naasoor'],
 'glorification':['shaheed','shahadat','qurbani','jihad','jehad','ghazi','badla','inteqam','intiqam','khoon','lahoo','marenge','mit jayenge'],
 'mobilization':['niklo','niklo','aao','utho','uth khare','dharna','harta','hartal','ihtijaj','ehtijaj','march','jalao','jalaao','ghero','gherao','band karo','protest','rally','sarko','sarkon'],
 'threat':['dekh lenge','dekhlenge','chhoren','choren','anjaam','anjam','tabah','khatam','sabak','maar denge','jala denge','aag laga'],
 'political':['siyasat','siyasi','hakoomat','hukoomat','government','fauj','army','adalat','election','intekhab','imran','khan','ptin','pdm','ppp','nawaz','maryam','establishment','martial'],
}
allkw=[(c,k) for c,ks in clusters.items() for k in ks]
def hits(t):
    s=' '+t+' '; found=set()
    for c,k in allkw:
        if k in s: found.add(c)
    return found
pool['clusters']=pool['norm'].map(hits)
pool['n_clusters']=pool['clusters'].map(len)
pool['relevant']=pool['n_clusters']>=1
# indicator-bearing cluster hits (exclude the generic 'political' gate)
core={'grievance','ingroup_outgroup','dehumanization','glorification','mobilization','threat'}
pool['n_core']=pool['clusters'].map(lambda s: len(s & core))

pool.drop(columns=['norm']).to_csv('pool_standardized.csv', index=False)
print('TOTAL pool (deduped):', len(pool))
print('by source:', dict(pool['source'].value_counts()))
print('relevant (>=1 cluster):', int(pool['relevant'].sum()),
      '| indicator-bearing (core>=1):', int((pool['n_core']>=1).sum()))
print('\ncore-cluster coverage (posts hitting each):')
for c in core:
    print(f'  {c:18s}', int(pool['clusters'].map(lambda s: c in s).sum()))
