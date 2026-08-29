#!/usr/bin/env python3
"""
Re-hydrate the RU-RAD-6 corpus with post text.

This repository releases LABELS ONLY (no source post text). Each row is keyed by
`tweet_id`, a deterministic hash of the normalized source text
(tweet_id = 'ru' + md5(normalized_text)[:10]). To attach text, obtain the two
public source datasets yourself and run this script; it recomputes the same
tweet_id from those sources and joins the released labels back onto the text.

Source datasets (obtain separately, under their own terms):
  * RUHSOLD (Rizwan et al., EMNLP 2020): task_1_{train,validation,test}.tsv and
    task_2_{...}.tsv, tab-separated (text<TAB>label), placed under RUHSOLD/
  * RU-HSD-30K (Bilal): 'final 30,000 dataset_romanurdu.csv' with a tweets/text
    column, placed under RUHSD30K/

Usage:
  python rehydrate.py \
      --ruhsold_dir RUHSOLD \
      --ru30k_csv "RUHSD30K/final 30,000 dataset_romanurdu.csv" \
      --labels data/roman_urdu_indicators_v1.csv \
      --out roman_urdu_indicators_v1_TEXT.csv
"""
import argparse, re, hashlib, os, pandas as pd

def norm(t):
    t = re.sub(r'http\S+', '', str(t))
    t = re.sub(r'\s+', ' ', t).strip().lower()
    return t

def tid(s):
    return 'ru' + hashlib.md5(s.encode()).hexdigest()[:10]

def load_ruhsold(d):
    frames = []
    for s in ['train', 'validation', 'test']:
        p = os.path.join(d, f'task_1_{s}.tsv')
        if os.path.exists(p):
            frames.append(pd.read_csv(p, sep='\t', header=None, names=['text', 'label'],
                          quoting=3, encoding='utf-8', on_bad_lines='skip').dropna())
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=['text'])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ruhsold_dir', required=True)
    ap.add_argument('--ru30k_csv', required=True)
    ap.add_argument('--labels', default='data/roman_urdu_indicators_v1.csv')
    ap.add_argument('--out', default='roman_urdu_indicators_v1_TEXT.csv')
    a = ap.parse_args()

    ru = load_ruhsold(a.ruhsold_dir)[['text']]
    r30 = pd.read_csv(a.ru30k_csv, encoding='latin-1', on_bad_lines='skip', engine='python')
    r30 = r30.rename(columns={'tweets': 'text'})[['text']]
    pool = pd.concat([ru, r30], ignore_index=True)
    pool['text'] = pool['text'].astype(str).str.strip()
    pool['norm'] = pool['text'].map(norm)
    pool = pool[pool['norm'].str.len() >= 8].drop_duplicates('norm')
    pool['tweet_id'] = pool['norm'].map(tid)
    id2text = dict(zip(pool['tweet_id'], pool['text']))

    lab = pd.read_csv(a.labels)
    lab['text'] = lab['tweet_id'].map(id2text)
    miss = int(lab['text'].isna().sum())
    cols = list(lab.columns); cols.insert(1, cols.pop(cols.index('text')))
    lab[cols].to_csv(a.out, index=False)
    print(f'Wrote {a.out}: {len(lab)} rows, {miss} without matched text.')
    if miss:
        print('Unmatched rows usually mean a source-file version/encoding mismatch; '
              'verify you have the exact public releases of RUHSOLD and RU-HSD-30K.')

if __name__ == '__main__':
    main()
