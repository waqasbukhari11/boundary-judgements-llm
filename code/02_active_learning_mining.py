# Part of the Roman Urdu indicator resource pipeline. Paths are relative to the source datasets (RUHSOLD, RU-HSD-30K).
import pandas as pd, numpy as np, re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import average_precision_score

gold=pd.read_csv('/mnt/user-data/outputs/gold_corpus_v1.csv')
pool=pd.read_csv('pool_standardized.csv')
rare=['glorification','dehumanization','threat']
used=set(gold['tweet_id']) | set(pd.read_csv('pilot_100_internal.csv')['tweet_id']) | set(pd.read_csv('calib_50_internal.csv')['tweet_id'])
unl=pool[~pool['tweet_id'].isin(used)].copy().reset_index(drop=True)

def clean(t): return re.sub(r'\s+',' ',str(t)).strip().lower()
gold['t']=gold['text'].map(clean); unl['t']=unl['text'].map(clean)

# shared TF-IDF fit on gold+unl vocab (char+word ngrams help for Roman Urdu spelling variation)
vec=TfidfVectorizer(analyzer='char_wb', ngram_range=(3,5), min_df=3, max_features=40000)
Xall=vec.fit(pd.concat([gold['t'],unl['t']]))
Xg=vec.transform(gold['t']); Xu=vec.transform(unl['t'])

scores={}
print('Ranker quality (5-fold CV average precision on the 1,000 labels):')
for c in rare:
    y=gold[c].values
    clf=LogisticRegression(max_iter=2000, class_weight='balanced', C=3.0)
    # CV AP as a sanity check that the ranker beats random (prevalence)
    cvp=cross_val_predict(clf, Xg, y, cv=5, method='predict_proba')[:,1]
    ap=average_precision_score(y, cvp); base=y.mean()
    clf.fit(Xg, y)
    scores[c]=clf.predict_proba(Xu)[:,1]
    print(f'  {c:16s} AP={ap:.3f}  (baseline prevalence {base:.3f}) -> lift x{ap/base:.1f}')

# rank unlabeled by each rare class; take enriched candidates
unl_sc=unl.copy()
for c in rare: unl_sc[c+'_score']=scores[c]
picked=set(); rows=[]
def take_top(col, n, tag):
    d=unl_sc[~unl_sc['tweet_id'].isin(picked)].sort_values(col, ascending=False)
    for _,r in d.head(n).iterrows():
        picked.add(r['tweet_id']); rows.append((r['tweet_id'], r['text'], tag, round(float(r[col]),3)))
# top candidates per rare class (enriched); glorification hardest so give it the most
take_top('glorification_score', 200, 'glorification')
take_top('dehumanization_score', 160, 'dehumanization')
take_top('threat_score', 160, 'threat')
mine=pd.DataFrame(rows, columns=['tweet_id','text','_target','_score']).drop_duplicates('tweet_id')
mine=mine.sample(frac=1, random_state=5).reset_index(drop=True)
mine.to_csv('mine_internal.csv', index=False)
print('\nmining batch size:', len(mine), '| by target:', mine['_target'].value_counts().to_dict())
print('score ranges:', {c: (round(scores[c].max(),2)) for c in rare})
