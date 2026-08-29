# REPLICATION

End-to-end guide to reproduce every reported result from raw inputs. Each result file in
`agreement/` is produced by a numbered script in `code/`. Nothing outside this folder is
needed except the two public source datasets and (for grounding) the ACLED export.

## 0. Inputs

| Input | Where to get it | Used by |
|---|---|---|
| RUHSOLD (Roman Urdu hate speech) | github.com/haroonshakeel/roman_urdu_hate_speech | 01 |
| RU-HSD-30K | github.com/Bilal4209/RU-HSD-30K | 01 |
| ACLED Pakistan export `pakistan_2021_2024.csv` | ACLED (acleddata.com), Pakistan 2021–2024 | 05 |
| `data/roman_urdu_indicators_v1.csv` | this folder (the labeled corpus) | 03, 04, hate-comparator |
| `data/train_ready.csv` | this folder (text + 5 labels + fold) | 03, 04 |
| `data/splits.csv` | this folder (frozen train/val/test) | all modeling |

Python: `pandas scikit-learn scipy iterative-stratification` (CPU steps); plus
`transformers==4.44.2 datasets accelerate torch` on a GPU for the transformer.

## 1. Pipeline (what produces what)

| Step | Script | Output |
|---|---|---|
| Build & relevance-filter pool | `code/01_build_pool.py` | standardized 39,458-post pool |
| Active-learning mining (rare classes) | `code/02_active_learning_mining.py` | ranked candidate lists |
| Baseline detectors (TF-IDF+LR) | (in-repo baseline routine) | `agreement/baseline_results.csv` |
| XLM-R v1 (**deprecated — failed run**) | `code/03_train_xlmr_colab.py` | do **not** use; kept for provenance |
| XLM-R v2 (per-indicator, correct) | `code/04_train_xlmr_v2_colab.py` | `xlmr_results_v2.csv` (run on GPU) |
| ACLED grounding | `code/05_acled_grounding.py` | `agreement/acled_grounding_results.csv`, `acled_cleavage_specificity.csv`, `acled_reference_gazetteer.csv` |
| Distinctiveness / hate comparator | (hate-comparator routine) | `agreement/distinctiveness.csv`, `hate_comparator.csv` |

> Note: XLM-R **v1 (03) failed to learn** (joint multi-label underfit; AUC-PR at base rate).
> The correct run is **v2 (04)**: five per-indicator binary models, positive oversampling,
> best checkpoint by validation AUC-PR. Only v2 numbers go in the paper.

## 2. Frozen splits (do not regenerate)
`data/splits.csv` fixes train (1,099) / val (194) / **test (227, all double-annotated)**,
multi-label stratified so every indicator has positives in each fold. Baselines and the
transformer use these exact splits so all numbers are directly comparable. Re-generating splits
would break comparability with the reported figures.

## 3. Result files → paper sections

| Result file | Paper section | Headline |
|---|---|---|
| `iaa_by_round.csv`, `IAA_REPORT.md` | §5 dataset reliability | pooled α = 0.96 (canonical 350-post subset); trajectory 0.79→0.96 |
| `label_distribution.csv` | §5 corpus | positives: ig 199 / grievance 78 / mobilization 60 / threat 39 / dehumanization 30 / glorification 10 |
| `baseline_results.csv` | §7.1 | TF-IDF+LR per-indicator P/R/F1/AUC-PR + bootstrap CIs |
| `xlmr_results_v2.csv` | §7.1 | XLM-R per-indicator (comparable to baseline) |
| `distinctiveness.csv` + `hate_comparator.csv`, `DISTINCTIVENESS_REPORT.md` | §7.2 | hate model (F1 0.87) is 7–8× worse than dedicated detectors on grievance/mobilization |
| `acled_grounding_results.csv` + `acled_cleavage_specificity.csv`, `GROUNDING_REPORT.md` | §7.4 | ig/dehum/grievance reference ACLED conflict actors ~2× (p<0.001); structured cleavage mapping |

## 4. Label policy (how gold was finalized)
- Full-run IAA subset (350): disagreements **adjudicated** against the guideline.
- Other double-annotated batches (mined 320, solo-2 200): **both-agree (intersection)** labels
  — robust to single-annotator drift (one solo-2 batch was over-marked, detected, re-labeled).
- Solo halves (single-annotator): that annotator's labels stand.

## 5. Reproduction order
1. `01_build_pool.py` → pool. 2. `02_active_learning_mining.py` → candidates (already annotated;
labels are in `roman_urdu_indicators_v1.csv`). 3. baseline routine → `baseline_results.csv`.
4. `04_train_xlmr_v2_colab.py` on GPU → `xlmr_results_v2.csv`. 5. hate-comparator →
`distinctiveness.csv` + `hate_comparator.csv`. 6. `05_acled_grounding.py` with the ACLED export →
grounding files. All numbers in the reports are reproduced by these steps on the frozen splits.

## 6. Ethics & scope (applies to any reuse)
Discourse-level, aggregate research only. Not for profiling, identifying, or acting against
individuals. See `../README.md` and `../taxonomy/indicator_taxonomy.md`.
