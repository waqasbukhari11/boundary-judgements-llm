# =============================================================================
# Phase 6 (v2) — XLM-RoBERTa PER-INDICATOR fine-tuning  [replaces v1]
# Fixes the failed joint run: trains 5 SEPARATE binary models, oversamples
# positives, evaluates every epoch, and keeps the BEST checkpoint by val AUC-PR.
#
# HOW TO RUN (Colab, GPU):
#   1. Runtime > Change runtime type > GPU.
#   2. Upload `train_ready.csv`.
#   3. Paste this whole file into a cell and run. (~30-50 min on a T4 for all 5.)
#   4. Download `xlmr_results_v2.csv` and send it back.
# Same frozen folds as the baseline, so results stay comparable.
# =============================================================================

!pip -q install transformers==4.44.2 datasets accelerate scikit-learn

import numpy as np, pandas as pd, torch, random
from torch.utils.data import WeightedRandomSampler
from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
                          TrainingArguments, Trainer)
from sklearn.metrics import average_precision_score, precision_recall_fscore_support

SEED=42; random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
LABELS=['ig_outgroup','grievance','mobilization','threat','dehumanization']
MODEL='xlm-roberta-base'; MAXLEN=128; EPOCHS=15; LR=2e-5

df=pd.read_csv('train_ready.csv')
tok=AutoTokenizer.from_pretrained(MODEL)
def make_ds(frame, col):
    import datasets as hfds
    e=tok(list(frame['text'].astype(str)), truncation=True, padding='max_length', max_length=MAXLEN)
    e['labels']=frame[col].astype(int).tolist()
    return hfds.Dataset.from_dict(e)

def ap_metric(eval_pred):
    logits,labels=eval_pred
    p=torch.softmax(torch.tensor(logits),dim=1)[:,1].numpy()
    return {'auc_pr': average_precision_score(labels,p) if labels.sum()>0 else 0.0}

# oversample positives so each minibatch sees them (per label)
class OverTrainer(Trainer):
    def __init__(self,*a,sample_w=None,**k): super().__init__(*a,**k); self.sample_w=sample_w
    def _get_train_sampler(self, *args, **kwargs):
        return WeightedRandomSampler(self.sample_w, len(self.sample_w), replacement=True)

def boot(y,s,thr,n=2000):
    idx=np.arange(len(y)); f=[]; a=[]
    for _ in range(n):
        b=np.random.choice(idx,len(idx),True); yb,sb=y[b],s[b]
        if yb.sum()==0: continue
        _,_,ff,_=precision_recall_fscore_support(yb,(sb>=thr).astype(int),average='binary',zero_division=0)
        f.append(ff); a.append(average_precision_score(yb,sb))
    return (np.nanpercentile(f,2.5),np.nanpercentile(f,97.5)),(np.nanpercentile(a,2.5),np.nanpercentile(a,97.5))

tr=df[df.fold=='train'].reset_index(drop=True); va=df[df.fold=='val'].reset_index(drop=True); te=df[df.fold=='test'].reset_index(drop=True)
rows=[]
for c in LABELS:
    print(f'\n===== {c} =====')
    # per-label oversampling weights (positives up-weighted to ~balance)
    y=tr[c].values.astype(int); w=np.where(y==1, (len(y)-y.sum())/max(y.sum(),1), 1.0)
    model=AutoModelForSequenceClassification.from_pretrained(MODEL, num_labels=2)
    args=TrainingArguments(output_dir=f'out_{c}', num_train_epochs=EPOCHS, learning_rate=LR,
        per_device_train_batch_size=16, per_device_eval_batch_size=32,
        eval_strategy='epoch', save_strategy='epoch', save_total_limit=1,
        load_best_model_at_end=True, metric_for_best_model='auc_pr', greater_is_better=True,
        warmup_ratio=0.1, weight_decay=0.01, seed=SEED, report_to='none', logging_steps=50)
    tr_ds=make_ds(tr,c); va_ds=make_ds(va,c); te_ds=make_ds(te,c)
    trn=OverTrainer(model=model,args=args,train_dataset=tr_ds,eval_dataset=va_ds,
                    compute_metrics=ap_metric, sample_w=torch.tensor(w,dtype=torch.double))
    trn.train()
    sva=torch.softmax(torch.tensor(trn.predict(va_ds).predictions),1)[:,1].numpy()
    ste=torch.softmax(torch.tensor(trn.predict(te_ds).predictions),1)[:,1].numpy()
    yva=va[c].values; yte=te[c].values
    bt,bf=0.5,-1
    for t in np.linspace(0.05,0.95,37):
        _,_,ff,_=precision_recall_fscore_support(yva,(sva>=t).astype(int),average='binary',zero_division=0)
        if ff>bf: bf,bt=ff,t
    p=(ste>=bt).astype(int)
    P,R,F,_=precision_recall_fscore_support(yte,p,average='binary',zero_division=0)
    AP=average_precision_score(yte,ste)
    (flo,fhi),(alo,ahi)=boot(yte,ste,bt)
    rows.append([c,round(P,3),round(R,3),round(F,3),f'[{flo:.2f},{fhi:.2f}]',round(AP,3),f'[{alo:.2f},{ahi:.2f}]',round(bt,2),round(yte.mean(),3)])
    print(f'{c}: F1={F:.3f} AUC-PR={AP:.3f} (base {yte.mean():.3f})')

res=pd.DataFrame(rows,columns=['indicator','precision','recall','f1','f1_95ci','auc_pr','auc_pr_95ci','threshold','base_rate'])
res.loc[len(res)]=['MACRO',round(res.precision.mean(),3),round(res.recall.mean(),3),round(res.f1.mean(),3),'',round(res.auc_pr.mean(),3),'','','']
print('\n', res.to_string(index=False))
res.to_csv('xlmr_results_v2.csv', index=False)
print('\nSaved xlmr_results_v2.csv — download and send back.')
