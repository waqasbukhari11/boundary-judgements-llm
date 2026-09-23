"""
06_twitter_validation_mining.py
Candidate mining for the independent Twitter validation corpus (Section 6.7).

Same high-recall keyword approach used for the original corpus (01_build_pool.py,
02_active_learning_mining.py), applied to a separately collected Twitter dataset
to build a candidate pool for independent annotation. Text is NOT redistributed;
this script documents the mining logic for reproducibility, applied by the
authors to their own local copy of the source data.
"""
import pandas as pd, re, hashlib

KW = {
 'ig_outgroup': ['ghaddar','gaddar','traitor','dushman','yahudi','agent','lifafa',
                 'patwari','youthia','bhikari','ghulam','namak haram','desh drohi'],
 'dehumanization': ['kutta','kuttay','kuttey','janwar','haiwan','keeray','suar',
                     'chuha','gandagi','keera','jaanwar'],
 'grievance': ['zulm','zulum','mazloom','na insafi','nainsafi','haq','mehroom',
               'ghasb','zyadti','bebasi','faryaad','sitam'],
 'glorification': ['shaheed','shahadat','jihad','ghazi','mujahid','qurbani',
                    'jaan qurban','shahadat mubarak'],
 'mobilization': ['niklo','nikal','sarak par','ao','aao','uth','jago','tayyar',
                   'call','march','dharna','ehtejaj','protest','band karo'],
 'threat': ['dekh lenge','maar','khatam','anjaam','badla','intiqam','tor',
            'nahi chorenge','sabaq sikha','khoon'],
}

def hits(text):
    t = str(text).lower()
    return [f"{ind}:{w}" for ind, words in KW.items() for w in words if w in t]

def build_candidates(df, text_col='text', id_cols=('Username','timestamp')):
    """df: local dataframe with a text column and identifying columns.
    Returns a text-free candidate table with a stable hashed tweet_id."""
    df = df.copy()
    df['norm'] = df[text_col].astype(str).str.lower().str.strip()
    df = df.drop_duplicates('norm').reset_index(drop=True)
    df['keyword_hits'] = df[text_col].apply(hits)
    df['n_hits'] = df.keyword_hits.apply(len)
    cand = df[df.n_hits > 0].copy()
    cand['tweet_id'] = cand.apply(
        lambda r: 'TW' + hashlib.md5(
            f"{r[id_cols[0]]}|{r[id_cols[1]]}|{r['norm']}".encode()).hexdigest()[:10],
        axis=1)
    return cand[['tweet_id','keyword_hits']]

if __name__ == '__main__':
    # df = pd.read_csv('<path to your local copy of the source dataset>')
    # candidates = build_candidates(df)
    # candidates.to_csv('candidate_pool.csv', index=False)
    pass
