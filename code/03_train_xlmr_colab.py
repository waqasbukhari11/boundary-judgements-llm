# =============================================================================
# Phase 6 — XLM-RoBERTa multi-label detector training + evaluation
# Roman Urdu violent-radicalization discourse indicators
#
# HOW TO RUN (Google Colab, GPU runtime):
#   1. Runtime > Change runtime type > GPU (T4 is fine).
#   2. Upload `train_ready.csv` (from data/) to the Colab session.
#   3. Paste this whole file into a cell (or upload and %run it) and run.
#   4. When it finishes, download `xlmr_results.csv` and send it back.
#
# Trains ONE shared XLM-RoBERTa encoder with 5 binary heads (multi-label) for:
#   ig_outgroup, grievance, mobilization, threat, dehumanization
# (glorification is intentionally excluded — reported descriptively.)
#
# Uses the SAME frozen train/val/test folds as the in-sandbox baselines, so the
# transformer numbers are directly comparable to the TF-IDF+LR baseline.
# =============================================================================

!pip -q install transformers==4.44.2 datasets accelerate scikit-learn iterative-stratification

import numpy as np, pandas as pd, torch, random
from torch import nn
from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
                          TrainingArguments, Trainer)
from sklearn.metrics import average_precision_score, precision_recall_fscore_support

SEED=42
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
LABELS=['ig_outgroup','grievance','mobilization','threat','dehumanization']
MODEL='xlm-roberta-base'
EPOCHS=8            # small data → a few epochs; early signal by epoch 4-6
MAXLEN=128
LR=2e-5

df=pd.read_csv('train_ready.csv')
tr=df[df.fold=='train'].reset_index(drop=True)
va=df[df.fold=='val'].reset_index(drop=True)
te=df[df.fold=='test'].reset_index(drop=True)
print('sizes', len(tr), len(va), len(te))

# class imbalance → pos_weight per label (from TRAIN only)
pos=tr[LABELS].sum().values.astype(float); neg=len(tr)-pos
pos_weight=torch.tensor(neg/np.clip(pos,1,None), dtype=torch.float)
print('pos_weight', dict(zip(LABELS, pos_weight.round().tolist())))

tok=AutoTokenizer.from_pretrained(MODEL)
def enc(frame):
    e=tok(list(frame['text'].astype(str)), truncation=True, padding='max_length', max_length=MAXLEN)
    e['labels']=frame[LABELS].values.astype('float32').tolist()
    return e
import datasets as hfds
dtr=hfds.Dataset.from_dict(enc(tr)); dva=hfds.Dataset.from_dict(enc(va)); dte=hfds.Dataset.from_dict(enc(te))

model=AutoModelForSequenceClassification.from_pretrained(
    MODEL, num_labels=len(LABELS), problem_type='multi_label_classification')

class WTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, **kw):
        labels=inputs.pop('labels')
        out=model(**inputs); logits=out.logits
        loss=nn.BCEWithLogitsLoss(pos_weight=pos_weight.to(logits.device))(logits, labels)
        return (loss, out) if return_outputs else loss

args=TrainingArguments(output_dir='out', num_train_epochs=EPOCHS, learning_rate=LR,
    per_device_train_batch_size=16, per_device_eval_batch_size=32,
    eval_strategy='epoch', save_strategy='no', logging_steps=25,
    warmup_ratio=0.1, weight_decay=0.01, seed=SEED, report_to='none')
trainer=WTrainer(model=model, args=args, train_dataset=dtr, eval_dataset=dva)
trainer.train()

def sig(x): return 1/(1+np.exp(-x))
sva=sig(trainer.predict(dva).predictions); ste=sig(trainer.predict(dte).predictions)
Yva=va[LABELS].values; Yte=te[LABELS].values

def boot(y,s,thr,n=2000):
    idx=np.arange(len(y)); f=[]; a=[]
    for _ in range(n):
        b=np.random.choice(idx,len(idx),True); yb,sb=y[b],s[b]
        if yb.sum()==0: continue
        _,_,ff,_=precision_recall_fscore_support(yb,(sb>=thr).astype(int),average='binary',zero_division=0)
        f.append(ff); a.append(average_precision_score(yb,sb))
    return (np.nanpercentile(f,2.5),np.nanpercentile(f,97.5)),(np.nanpercentile(a,2.5),np.nanpercentile(a,97.5))

rows=[]
for i,c in enumerate(LABELS):
    # tune threshold on val
    bt,bf=0.5,-1
    for t in np.linspace(0.05,0.95,37):
        _,_,ff,_=precision_recall_fscore_support(Yva[:,i],(sva[:,i]>=t).astype(int),average='binary',zero_division=0)
        if ff>bf: bf,bt=ff,t
    p=(ste[:,i]>=bt).astype(int)
    P,R,F,_=precision_recall_fscore_support(Yte[:,i],p,average='binary',zero_division=0)
    AP=average_precision_score(Yte[:,i],ste[:,i])
    (flo,fhi),(alo,ahi)=boot(Yte[:,i],ste[:,i],bt)
    rows.append([c,round(P,3),round(R,3),round(F,3),f'[{flo:.2f},{fhi:.2f}]',round(AP,3),f'[{alo:.2f},{ahi:.2f}]',round(bt,2)])
res=pd.DataFrame(rows,columns=['indicator','precision','recall','f1','f1_95ci','auc_pr','auc_pr_95ci','threshold'])
# macro
res.loc[len(res)]=['MACRO',round(res.precision.mean(),3),round(res.recall.mean(),3),round(res.f1.mean(),3),'',round(res.auc_pr.mean(),3),'','']
print(res.to_string(index=False))
res.to_csv('xlmr_results.csv', index=False)
print('\nSaved xlmr_results.csv — download this and send it back.')
