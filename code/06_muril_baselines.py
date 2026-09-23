# =====================================================================
# mBERT / MuRIL baseline for RU-RAD-6 — CORRECTED VERSION
# Fixes vs previous run: (1) uses the actual test fold (fold=='test', n=227),
# not the IAA subset; (2) uses class-weighted loss during fine-tuning, so
# rare indicators (threat, dehumanization) aren't just predicted as all-negative.
# =====================================================================

!pip install transformers datasets scikit-learn -q

import pandas as pd, numpy as np, torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import TrainingArguments, Trainer
from sklearn.metrics import average_precision_score
import torch.nn as nn

MODEL = "google/muril-base-cased"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print("device:", DEVICE)
tok = AutoTokenizer.from_pretrained(MODEL)

class TextDS(torch.utils.data.Dataset):
    def __init__(self, texts, labels):
        self.enc = tok(list(texts), truncation=True, padding=True, max_length=128)
        self.labels = list(labels)
    def __len__(self): return len(self.labels)
    def __getitem__(self, i):
        item = {k: torch.tensor(v[i]) for k,v in self.enc.items()}
        item['labels'] = torch.tensor(self.labels[i], dtype=torch.long)
        return item

class WeightedTrainer(Trainer):
    """Cross-entropy with class weights = inverse frequency, matching
    sklearn's class_weight='balanced' used for the TF-IDF baselines."""
    def __init__(self, *args, class_weights=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = class_weights
    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.logits
        loss_fct = nn.CrossEntropyLoss(weight=self.class_weights.to(logits.device))
        loss = loss_fct(logits, labels)
        return (loss, outputs) if return_outputs else loss

def train_binary(texts, labels, epochs=4, lr=2e-5):
    from sklearn.model_selection import train_test_split
    labels = list(labels)
    Xtr, Xval, ytr, yval = train_test_split(
        texts, labels, test_size=0.15, random_state=42,
        stratify=labels if min(pd.Series(labels).value_counts())>1 else None)
    n0, n1 = ytr.count(0), ytr.count(1)
    # inverse-frequency weights, same spirit as class_weight='balanced'
    w0 = len(ytr) / (2*max(n0,1)); w1 = len(ytr) / (2*max(n1,1))
    weights = torch.tensor([w0, w1], dtype=torch.float)
    print(f"    class weights: neg={w0:.2f} pos={w1:.2f}  (train n_pos={n1}/{len(ytr)})")

    model = AutoModelForSequenceClassification.from_pretrained(MODEL, num_labels=2).to(DEVICE)
    args = TrainingArguments(
        output_dir="/tmp/out", num_train_epochs=epochs,
        per_device_train_batch_size=16, per_device_eval_batch_size=32,
        learning_rate=lr, eval_strategy="epoch", save_strategy="no",
        logging_steps=50, report_to=[])
    trainer = WeightedTrainer(model=model, args=args, class_weights=weights,
                       train_dataset=TextDS(Xtr, ytr), eval_dataset=TextDS(Xval, yval))
    trainer.train()
    return model

def score(model, texts, batch_size=32):
    model.eval(); probs = []
    with torch.no_grad():
        for i in range(0, len(texts), batch_size):
            batch = list(texts[i:i+batch_size])
            enc = tok(batch, truncation=True, padding=True, max_length=128, return_tensors='pt').to(DEVICE)
            p = torch.softmax(model(**enc).logits, dim=1)[:,1].cpu().numpy()
            probs.extend(p.tolist())
    return np.array(probs)

# =====================================================================
# STEP 1 — hate-speech proxy, trained on RUHSOLD
# =====================================================================
ruhsold = pd.read_csv('ruhsold_coarse.csv').dropna(subset=['tweet'])
print(f"RUHSOLD: {len(ruhsold)} rows")
proxy_model = train_binary(ruhsold.tweet.tolist(), ruhsold.label.tolist(), epochs=3)

# =====================================================================
# STEP 2 — dedicated per-indicator detectors, trained ONLY on the
# 'train' fold of RU-RAD-6 (not train+val+test combined) — matches how
# the TF-IDF baselines were fit, so the test-fold comparison is fair
# =====================================================================
rurad = pd.read_csv('roman_urdu_indicators_v1.csv').dropna(subset=['text'])
splits = pd.read_csv('splits.csv')   # tweet_id, fold  (train/val/test)
rurad = rurad.merge(splits, on='tweet_id', how='left')
print(rurad.fold.value_counts())

train_rows = rurad[rurad.fold == 'train']
test_rows  = rurad[rurad.fold == 'test']
print(f"train n={len(train_rows)}  test n={len(test_rows)}  (paper reports test n=227)")

DEDICATED_IND = ['ig_outgroup','grievance','mobilization','threat','dehumanization']
dedicated_models = {}
for ind in DEDICATED_IND:
    print(f"\n--- training dedicated detector: {ind} ---")
    dedicated_models[ind] = train_binary(train_rows.text.tolist(), train_rows[ind].tolist(), epochs=4)

# =====================================================================
# STEP 3 — evaluate on the ACTUAL test fold (n=227), compare to Table 6
# original TF-IDF dedicated AUC-PR: ig_outgroup .532, grievance .429,
# mobilization .441, threat .315, dehumanization .142
# =====================================================================
print(f"\nRU-RAD-6 TEST-FOLD evaluation (n={len(test_rows)}) — compare to Table 6")
for ind in DEDICATED_IND:
    y = test_rows[ind].values
    if y.sum() < 3:
        print(f"  {ind:16s} too few positives, skip"); continue
    p = score(dedicated_models[ind], test_rows.text.tolist())
    ap = average_precision_score(y, p)
    print(f"  {ind:16s} MuRIL AUC-PR = {ap:.3f}   (n_pos={int(y.sum())}/{len(y)})")

# =====================================================================
# STEP 4 — coverage-gap replication on the independent Twitter corpus
# =====================================================================
twitter = pd.read_csv('gold_corpus_1134.csv').dropna(subset=['text'])
twitter['muril_hate_proxy_score'] = score(proxy_model, twitter.text.tolist())

print(f"\nCoverage-gap replication (MuRIL), Twitter corpus n={len(twitter)}")
print(f"{'indicator':16s}{'positives':>10s}{'proxy_AP':>12s}{'dedicated_AP':>14s}{'gap':>8s}")
rows = []
for ind in DEDICATED_IND:
    y = twitter[ind].values
    n_pos = int(y.sum())
    if n_pos < 3:
        print(f"{ind:16s}{n_pos:10d}  -- too few positives --"); continue
    ded_p = score(dedicated_models[ind], twitter.text.tolist())
    proxy_ap = average_precision_score(y, twitter.muril_hate_proxy_score.values)
    ded_ap = average_precision_score(y, ded_p)
    gap = ded_ap/proxy_ap if proxy_ap>0 else np.nan
    rows.append((ind, n_pos, proxy_ap, ded_ap, gap))
    print(f"{ind:16s}{n_pos:10d}{proxy_ap:12.3f}{ded_ap:14.3f}{gap:8.1f}x")

pd.DataFrame(rows, columns=['indicator','positives','proxy_ap','dedicated_ap','gap']).to_csv(
    'muril_coverage_gap_results.csv', index=False)

from google.colab import files
files.download('muril_coverage_gap_results.csv')
print("\nSend back: the Step 3 test-fold numbers (printed above) and this CSV.")
