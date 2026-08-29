# LLM Evaluation (manuscript Section 7)

Prompted large language models evaluated as annotators against the RU-RAD-6
human gold standard on the held-out test fold (n = 227) — the same fold on
which the supervised detectors were scored.

## Design

| | |
|---|---|
| Models | Qwen2.5-7B-Instruct, Llama-3.1-8B-Instruct, Qwen2.5-72B-Instruct |
| Quantisation | 4-bit NF4 for the 7-8B models; the 72B ran via hosted inference |
| Decoding | greedy (`do_sample=False`) — deterministic |
| Conditions | zero_shot, few_shot (5 examples), taxonomy (full definitions + boundary rules) |
| Test fold | 227 posts, 70 gold positives across six indicators |

The two models are from different families and organisations, so shared
behaviour cannot be attributed to a single training pipeline. The **taxonomy**
condition is the substitution test: the model receives exactly the specification
the human annotators worked from, including boundary rules R1, R2, R3 and R6
verbatim.

The cross-model comparison uses the taxonomy condition. The prompt-condition
comparison (Table 16) was run on Qwen2.5-7B only; prompt effects were not tested
across model families.

## Files in `outputs/`

| File | Contents |
|---|---|
| `qwen2.5-7b__taxonomy__testfold.csv` | Per-post predictions, raw model output, parse status |
| `llama3.1-8b__taxonomy__testfold.csv` | As above |
| `qwen2.5-7b__zero_shot.csv` | Zero-shot condition |
| `qwen2.5-7b__few_shot.csv` | Few-shot condition |
| `qwen2.5-7b__eval.csv`, `llama3.1-8b__eval.csv` | Per-indicator precision/recall/F1 |
| `llm_comparison.csv` | F1 by indicator and model |

Each prediction file carries `tweet_id`, `raw` (verbatim model output), `status`
(`ok` / `refusal` / `malformed`), and six binary indicator columns.

## Headline results

- Both models over-produce labels: Qwen 3.5×, Llama 6.3× the gold positive count
- Human annotators leave 78% of posts unlabelled; the models leave 15–17%
- Mean inter-model Cohen's κ = 0.242, against human α = 0.963
- 127 shared false positives — both models positive, gold negative
- Zero refusals and zero malformed outputs in either run
- Few-shot (macro-F1 0.213) beats taxonomy definitions (0.172) and zero-shot (0.145)
- Scale mitigates but does not resolve: Qwen2.5-72B reaches 3.1x over-production
  and macro-F1 0.242, leaving 47% of posts unlabelled against the human 78%
- The residual failure concentrates on rare, boundary-dependent indicators:
  recall 1.000 on threat at 6.4x over-production
- Agreement stays low across all three: pairwise kappa 0.242, 0.261, 0.281;
  58 false positives are shared by all three models against 70 gold positives

## Reproducing

Requires the corpus **with text**, which is not redistributed. Run
`code/rehydrate.py` first (see main README).

```bash
python code/06_llm_annotation.py --model qwen2.5-7b  --condition taxonomy
python code/06_llm_annotation.py --model llama3.1-8b --condition taxonomy
python code/06_llm_annotation.py --evaluate     # regenerates Tables 13–16
```

Scoring alone needs no GPU and runs from the prediction files already present:

```bash
python code/06_llm_annotation.py --evaluate
```
