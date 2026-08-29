# =============================================================================
# §7.4 — ACLED grounding (external construct validation, NON-temporal)
#
# Tests whether indicator-bearing Roman Urdu discourse references the same
# conflict actors / themes that ACLED independently documents for Pakistan,
# with a null comparison (indicator-negative discourse) and an indicator-
# specific mapping. This is THEMATIC construct validity, not prediction.
#
# INPUTS (place in the same folder):
#   - pakistan_2021_2024.csv        (the ACLED export)
#   - gold_corpus_final.csv         (from data/)
# RUN:  python 05_acled_grounding.py
# OUTPUT: acled_grounding_results.csv, acled_reference_gazetteer.csv
# =============================================================================
import pandas as pd, numpy as np, re
from scipy.stats import chi2_contingency, fisher_exact

LABELS=['ig_outgroup','dehumanization','grievance','glorification','mobilization','threat']

acled=pd.read_csv('pakistan_2021_2024.csv')
acled.columns=[c.strip().lower() for c in acled.columns]
print('ACLED rows:', len(acled), '| columns:', list(acled.columns)[:20])

# ---- 1. Build the conflict gazetteer from ACLED ----------------------------
def col(*names):
    for n in names:
        if n in acled.columns: return acled[n].astype(str)
    return pd.Series(['']*len(acled))

actors = pd.concat([col('actor1'), col('actor2'), col('assoc_actor_1'), col('assoc_actor_2')])
actors = actors[actors.str.len()>2].value_counts().head(60)
regions = col('admin1').value_counts().head(15)
etypes  = col('event_type').value_counts()
subtypes= col('sub_event_type').value_counts()

# curated match terms likely to appear (in English/acronym form) in Roman Urdu tweets
# (ACLED actor strings are English; tweets use the same acronyms/leader names)
def terms_from(series, minlen=3):
    out=set()
    for s in series.index:
        for tok in re.split(r'[^A-Za-z]+', s.lower()):
            if len(tok)>=minlen and tok not in {'the','and','group','forces','military','party','militia','police','state'}:
                out.add(tok)
    return out
gaz = terms_from(actors) | terms_from(regions)
# always-relevant conflict/actor cues (Pakistan context) — extend as needed
gaz |= {'ttp','taliban','tehreek','ptm','baloch','bla','sipah','lashkar','jaish','isis','daesh',
        'pti','pdm','ppp','pmln','mqm','jui','imran','maryam','nawaz','bilawal','army','fauj',
        'kashmir','waziristan','balochistan','karachi','quetta','peshawar','fc','rangers'}
pd.DataFrame({'term':sorted(gaz)}).to_csv('acled_reference_gazetteer.csv', index=False)
print(f'gazetteer terms: {len(gaz)}')

# map each ACLED event to a coarse cleavage (for indicator-specificity)
def cleavage(row):
    s=(str(row.get('actor1',''))+' '+str(row.get('actor2',''))+' '+str(row.get('notes',''))).lower()
    if any(k in s for k in ['ttp','taliban','tehreek','lashkar','jaish','isis','daesh','militant']): return 'militant'
    if any(k in s for k in ['sunni','shia','sectarian','sipah','ahmad']): return 'sectarian'
    if any(k in s for k in ['baloch','pashtun','ptm','muhajir','ethnic','bla']): return 'ethnic'
    if any(k in s for k in ['pti','pdm','ppp','pmln','mqm','jui','political party','protesters']): return 'political'
    return 'other'
if 'event_type' in acled.columns:
    acled['cleavage']=acled.apply(cleavage, axis=1)
    print('ACLED cleavage mix:', acled['cleavage'].value_counts().to_dict())

# ---- 2. Reference test: indicator-positive vs negative -----------------------
g=pd.read_csv('gold_corpus_final.csv')
pat=re.compile(r'\b('+'|'.join(sorted(map(re.escape,gaz), key=len, reverse=True))+r')\b', re.I)
g['refs_acled']=g['text'].astype(str).str.contains(pat).astype(int)
base_rate=g['refs_acled'].mean()
print(f'\nOverall ACLED-reference rate in corpus: {base_rate:.1%}')

rows=[]
for c in LABELS:
    pos=g[g[c]>0]['refs_acled']; neg=g[g[c]==0]['refs_acled']
    ct=np.array([[pos.sum(),len(pos)-pos.sum()],[neg.sum(),len(neg)-neg.sum()]])
    try: _,p,_,_=chi2_contingency(ct)
    except Exception: _,p=fisher_exact(ct)
    lift = (pos.mean()/neg.mean()) if neg.mean()>0 else np.nan
    rows.append([c,len(pos),round(pos.mean(),3),round(neg.mean(),3),round(lift,2),round(p,4)])
res=pd.DataFrame(rows,columns=['indicator','positives','ref_rate_pos','ref_rate_neg','lift','p_value'])
res.to_csv('acled_grounding_results.csv', index=False)
print('\nDo indicator-positive tweets reference ACLED conflict actors/themes more than negative ones?')
print(res.to_string(index=False))
print('\nlift>1 with small p = indicator discourse is anchored in the real conflict landscape (construct validity).')
