"""
06_llm_annotation.py — Prompted LLMs as annotators (manuscript Section 7)

Evaluates instruction-tuned multilingual LLMs on the RU-RAD-6 held-out test
fold (n = 227), the same fold on which the supervised detectors were scored.

Design
------
  Models      Qwen2.5-7B-Instruct, Llama-3.1-8B-Instruct
              (different families, so shared behaviour is not attributable
              to one training pipeline)
  Decoding    greedy, do_sample=False, 4-bit NF4 quantisation -> deterministic
  Conditions  zero_shot  : task framing + indicator names only
              few_shot   : + five labelled examples
              taxonomy   : + full indicator definitions incl. boundary rules
                           R1, R2, R3, R6 verbatim from the annotation guideline

The taxonomy condition is the substitution test: the model receives exactly
the specification the human annotators worked from. The cross-model comparison
uses taxonomy; the prompt-condition comparison was run on Qwen only.

Requirements
------------
  GPU (T4 sufficient), a Hugging Face token, and:
      data/roman_urdu_indicators_v1.csv    (gold labels; text via rehydrate.py)
      data/splits.csv                      (fold assignment)

Note: this script needs the corpus WITH text. Post text is not redistributed
(see README); reconstruct it locally with code/rehydrate.py first.

Usage
-----
      python 06_llm_annotation.py --model qwen2.5-7b --condition taxonomy
      python 06_llm_annotation.py --model llama3.1-8b --condition taxonomy
      python 06_llm_annotation.py --evaluate        # scores everything present
"""
import os, re, json, gc, glob, argparse
import numpy as np, pandas as pd

INDICATORS = ["ig_outgroup", "dehumanization", "grievance",
              "glorification", "mobilization", "threat"]
ID_COL, TEXT_COL = "tweet_id", "text"

MODEL_IDS = {
    "qwen2.5-7b":  "Qwen/Qwen2.5-7B-Instruct",
    "llama3.1-8b": "meta-llama/Llama-3.1-8B-Instruct",
}

# ── indicator definitions: verbatim from guidelines/annotation_guidelines_v1_1_FINAL.md
INDICATOR_DEFS = {
 "ig_outgroup": "In-group vs out-group framing: divides the world into a virtuous 'us' and an opposed, illegitimate 'them' framed as in conflict. Includes calling a named group traitor/ghaddar/enemy, 'real [nation/faith]' exclusion tests, and an implied out-group ('they oppress us'). NOT ordinary we/us pride with no adversary, and NOT mere criticism of a policy or leader.",
 "dehumanization": "Denies human or moral status to a GROUP, or frames people as vermin, insects, animals, subhuman, disease, or evil-by-nature in a way that invites their exclusion or harm. NOT a single animal slur aimed at one person in a quarrel, and NOT in-group self-defence.",
 "grievance": "The in-group, OR a solidarity group the author identifies or sympathizes with, is framed as oppressed, wronged, deprived, or denied justice (collective victimhood). NOT personal complaints, NOT merely blaming or taunting a target without a victim frame, and NOT neutral news reporting of suffering.",
 "glorification": "Praises, celebrates, or morally justifies NON-STATE, sectarian, or militant violence or its actors, including martyrdom or heroism framing. NOT ordinary patriotic commemoration of the state armed forces, and NOT reporting or mourning violence without endorsing it.",
 "mobilization": "The post itself urges the audience to take or join contentious collective action: direct imperatives like 'come out', 'join', 'we must march', 'rise up', or a militant call to fight. NOT merely reporting or describing that a protest or struggle is happening.",
 "threat": "An explicit threat, warning of harm, or stated intent to harm a target: direct calls to harm, conditional warnings of harm ('or else you will be finished'), or revenge framing. NOT disagreement or criticism without intent to harm.",
}

FEWSHOT = [
 {"text": "yaar aaj mausam kitna acha hai, chai peene ka dil kar raha hai", "labels": []},
 {"text": "hamesha hamare logon par hi zulm hota hai, koi hamari faryaad nahi sunta", "labels": ["grievance"]},
 {"text": "chup mat raho, kal sab apne haq ke liye sarak par niklo", "labels": ["mobilization"]},
 {"text": "ye log insaan nahi keeray makoray hain, inko yahan rehne ka koi haq nahi", "labels": ["ig_outgroup", "dehumanization"]},
 {"text": "niklo aur in gharon ko jala do, inhe sabaq sikhana hai", "labels": ["mobilization", "threat"]},
]

HEADER = ("You are labeling short Roman Urdu (Latin-script Urdu, code-mixed) social "
          "media posts for six discourse indicators. A post may have zero, one, or "
          "several indicators. Most posts have NONE - only label an indicator when "
          "the rule clearly applies. Return ONLY a JSON object: "
          '{"labels": [<indicator names present>]}. Valid indicator names: '
          + ", ".join(INDICATORS) + ".")

def p_zero(t):
    return f"{HEADER}\n\nPost: {t}\nJSON:"

def p_few(t):
    ex = "\n".join(f'Post: {e["text"]}\nJSON: {{"labels": {json.dumps(e["labels"])}}}'
                   for e in FEWSHOT)
    return f"{HEADER}\n\nExamples:\n{ex}\n\nPost: {t}\nJSON:"

def p_tax(t):
    defs = "\n".join(f"- {k}: {v}" for k, v in INDICATOR_DEFS.items())
    return f"{HEADER}\n\nIndicator definitions:\n{defs}\n\nPost: {t}\nJSON:"

PROMPTS = {"zero_shot": p_zero, "few_shot": p_few, "taxonomy": p_tax}

REFUSAL = re.compile(r"\b(i can(?:not|'t)|i am unable|i'm unable|as an ai|"
                     r"i won'?t|cannot assist|can't help|not able to)\b", re.I)

def parse_labels(raw):
    """Parse model output to (labels, status). status in {ok, refusal, malformed}."""
    if not raw or not raw.strip():
        return [], "malformed"
    if REFUSAL.search(raw) and "{" not in raw:
        return [], "refusal"
    m = re.search(r'\{.*\}', raw, re.S)
    if not m:
        found = [i for i in INDICATORS if re.search(rf'\b{re.escape(i)}\b', raw)]
        return (found, "ok") if found else ([], "malformed")
    try:
        labs = [l for l in json.loads(m.group(0)).get("labels", []) if l in INDICATORS]
        return labs, "ok"
    except Exception:
        found = [i for i in INDICATORS if re.search(rf'\b{re.escape(i)}\b', m.group(0))]
        return (found, "ok") if found else ([], "malformed")


def load_test_fold():
    gold = pd.read_csv("data/roman_urdu_indicators_v1.csv")
    sp   = pd.read_csv("data/splits.csv")
    test = set(sp.loc[sp.fold == "test", ID_COL])
    df = gold[gold[ID_COL].isin(test)].reset_index(drop=True)
    assert len(df) == 227, f"expected 227 test posts, got {len(df)}"
    if TEXT_COL not in df.columns:
        raise SystemExit("Post text absent. Run code/rehydrate.py first — text is "
                         "not redistributed (see README).")
    return df


def run(model_key, condition, outdir="llm_evaluation/outputs"):
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
    from tqdm import tqdm

    os.makedirs(outdir, exist_ok=True)
    df = load_test_fold()
    mid = MODEL_IDS[model_key]

    bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                             bnb_4bit_compute_dtype=torch.float16)
    tok = AutoTokenizer.from_pretrained(mid)
    model = AutoModelForCausalLM.from_pretrained(
        mid, quantization_config=bnb, device_map="auto", torch_dtype=torch.float16)

    @torch.inference_mode()
    def gen(prompt, max_new_tokens=64):
        enc = tok.apply_chat_template([{"role": "user", "content": prompt}],
            add_generation_prompt=True, return_tensors="pt",
            return_dict=True).to(model.device)
        out = model.generate(**enc, max_new_tokens=max_new_tokens,
                             do_sample=False, pad_token_id=tok.eos_token_id)
        return tok.decode(out[0][enc["input_ids"].shape[1]:], skip_special_tokens=True)

    pfn = PROMPTS[condition]
    rows = []
    for _, r in tqdm(df.iterrows(), total=len(df), desc=f"{model_key}/{condition}"):
        raw = gen(pfn(str(r[TEXT_COL])))
        labs, status = parse_labels(raw)
        row = {ID_COL: r[ID_COL], "raw": raw, "status": status}
        for ind in INDICATORS:
            row[ind] = int(ind in labs)
        rows.append(row)

    path = f"{outdir}/{model_key}__{condition}__testfold.csv"
    pd.DataFrame(rows).to_csv(path, index=False)
    print("saved:", path)
    del model, tok; gc.collect(); torch.cuda.empty_cache()


def evaluate(outdir="llm_evaluation/outputs"):
    """Reproduce manuscript Tables 13-16 from prediction files."""
    from sklearn.metrics import precision_recall_fscore_support, f1_score, cohen_kappa_score

    gold = pd.read_csv("data/roman_urdu_indicators_v1.csv")
    sp   = pd.read_csv("data/splits.csv")
    test = set(sp.loc[sp.fold == "test", ID_COL])
    g = gold[gold[ID_COL].isin(test)][[ID_COL] + INDICATORS]

    def boot_ci(y, yh, n=2000, seed=42):
        rng = np.random.default_rng(seed)
        y, yh = np.asarray(y), np.asarray(yh)
        s = [f1_score(y[i], yh[i], zero_division=0)
             for i in (rng.integers(0, len(y), len(y)) for _ in range(n))]
        return np.percentile(s, [2.5, 97.5])

    # ---- Table 13: per-model F1 with bootstrap CIs -----------------------
    print("\n=== Table 13: detection performance, taxonomy prompt ===")
    preds = {}
    for f in sorted(glob.glob(f"{outdir}/*__taxonomy__testfold.csv")):
        key = os.path.basename(f).split("__")[0]
        p = pd.read_csv(f)
        p = p[p[ID_COL].isin(test)]
        preds[key] = g.merge(p[[ID_COL]+INDICATORS], on=ID_COL, suffixes=("_g", "_p"))
        rows = []
        for ind in INDICATORS:
            y, yh = preds[key][ind+"_g"], preds[key][ind+"_p"]
            pr, rc, f1, _ = precision_recall_fscore_support(
                y, yh, average="binary", zero_division=0)
            lo, hi = boot_ci(y, yh)
            rows.append({"indicator": ind, "n_pos": int(y.sum()),
                         "n_pred": int(yh.sum()), "precision": round(pr, 3),
                         "recall": round(rc, 3), "f1": round(f1, 3),
                         "ci_low": round(lo, 3), "ci_high": round(hi, 3)})
        d = pd.DataFrame(rows)
        print(f"\n{key}"); print(d.to_string(index=False))
        print(f"macro-F1: {d.f1.mean():.3f}")
        d.to_csv(f"{outdir}/{key}__eval_with_ci.csv", index=False)

    if len(preds) < 2:
        print("\n(run both models for Tables 14-15)"); return

    ka, kb = list(preds)
    A, B = preds[ka], preds[kb]

    # ---- Table 14: label production --------------------------------------
    print("\n=== Table 14: label production ===")
    t14 = []
    for nm, d, sfx in [("gold", A, "_g"), (ka, A, "_p"), (kb, B, "_p")]:
        row = {"system": nm}
        for ind in INDICATORS:
            row[ind] = int(d[ind+sfx].sum())
        row["total"] = sum(row[i] for i in INDICATORS)
        t14.append(row)
    t14 = pd.DataFrame(t14)
    print(t14.to_string(index=False))
    t14.to_csv(f"{outdir}/table14_label_production.csv", index=False)

    print("\nmean labels per post / posts with no indicator:")
    for nm, d, sfx in [("gold", A, "_g"), (ka, A, "_p"), (kb, B, "_p")]:
        s = d[[i+sfx for i in INDICATORS]].sum(axis=1)
        print(f"  {nm:14s} mean={s.mean():.2f}  none={int((s==0).sum())}/{len(d)} "
              f"({(s==0).mean():.0%})")

    # ---- Table 15: inter-model agreement + shared FP ---------------------
    print("\n=== Table 15: inter-model agreement and shared false positives ===")
    M = A[[ID_COL] + [i+"_g" for i in INDICATORS] + [i+"_p" for i in INDICATORS]].merge(
        B[[ID_COL] + [i+"_p" for i in INDICATORS]].rename(
            columns={i+"_p": i+"_b" for i in INDICATORS}), on=ID_COL)
    rows, tot_fp = [], 0
    for ind in INDICATORS:
        k = cohen_kappa_score(M[ind+"_p"], M[ind+"_b"])
        both = int(((M[ind+"_p"] == 1) & (M[ind+"_b"] == 1)).sum())
        fp = int(((M[ind+"_g"] == 0) & (M[ind+"_p"] == 1) & (M[ind+"_b"] == 1)).sum())
        tot_fp += fp
        rows.append({"indicator": ind, "kappa": round(k, 3),
                     "both_positive": both, "shared_fp": fp,
                     "gold_pos": int(M[ind+"_g"].sum())})
    t15 = pd.DataFrame(rows)
    print(t15.to_string(index=False))
    print(f"mean kappa: {t15.kappa.mean():.3f}   total shared FP: {tot_fp}")
    t15.to_csv(f"{outdir}/table15_agreement.csv", index=False)

    # ---- Table 16: prompt conditions (single model) ----------------------
    conds = {c: f"{outdir}/qwen2.5-7b__{c}.csv" for c in ("zero_shot", "few_shot")}
    conds["taxonomy"] = f"{outdir}/qwen2.5-7b__taxonomy__testfold.csv"
    if all(os.path.exists(v) for v in conds.values()):
        print("\n=== Table 16: prompt-condition comparison (Qwen2.5-7B) ===")
        rows = []
        for cond, path in conds.items():
            p = pd.read_csv(path); p = p[p[ID_COL].isin(test)]
            m = g.merge(p[[ID_COL]+INDICATORS], on=ID_COL, suffixes=("_g", "_p"))
            for ind in INDICATORS:
                _, _, f1, _ = precision_recall_fscore_support(
                    m[ind+"_g"], m[ind+"_p"], average="binary", zero_division=0)
                rows.append({"condition": cond, "indicator": ind,
                             "f1": round(f1, 3), "n_pred": int(m[ind+"_p"].sum())})
        t16 = pd.DataFrame(rows)
        print(t16.pivot(index="indicator", columns="condition", values="f1").to_string())
        print("\nmacro-F1:"); print(t16.groupby("condition").f1.mean().round(3).to_string())
        print("\npredicted positives (gold = 70):")
        print(t16.groupby("condition").n_pred.sum().to_string())
        t16.to_csv(f"{outdir}/table16_prompt_conditions.csv", index=False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", choices=list(MODEL_IDS))
    ap.add_argument("--condition", choices=list(PROMPTS), default="taxonomy")
    ap.add_argument("--evaluate", action="store_true")
    a = ap.parse_args()
    if a.evaluate:
        evaluate()
    elif a.model:
        run(a.model, a.condition)
    else:
        ap.error("give --model or --evaluate")
