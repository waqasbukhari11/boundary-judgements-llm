# Roman Urdu Violent-Radicalization Discourse Indicators — Resource Package

A theory-grounded, multi-label annotated corpus of **six discourse indicators** associated
with violent-radicalization language in code-mixed **Roman Urdu**, built by re-labeling
existing public Roman Urdu hate-speech datasets against a purpose-built taxonomy.

This package is the **resource contribution** of the paper. It contains the dataset, the
validated annotation guideline, the inter-annotator agreement (IAA) evidence, the taxonomy
definitions, and the code used to construct and mine the corpus. It is designed to be
released alongside the article and cited.

> **Scope and ethics.** This resource labels *discourse markers* at the level of individual
> posts for aggregate research. It does **not** identify or classify individuals as
> radicalized, infer intent, or support enforcement. See `taxonomy/` and the ethics note
> below.


**Repository:** [GitHub repository URL to be added upon acceptance]  
**Citation:** see `CITATION.md` (authors: Shah, Arshad, Alsaleh, Nazir, Chaudhary; corresponding: A. Alsaleh).

---

## What's in here

```
roman_urdu_indicators_resource/
├── README.md                     ← you are here
├── data/
│   ├── roman_urdu_indicators_v1.csv   ← LABELS ONLY (1,520 posts, 6 indicators); text via code/rehydrate.py
│   └── label_distribution.csv         ← positives + prevalence per indicator
├── guidelines/
│   └── annotation_guidelines_v1_1_FINAL.md   ← the definitive annotation manual
├── agreement/
│   ├── iaa_by_round.csv               ← per-round, per-indicator Krippendorff's α
│   └── IAA_REPORT.md                  ← narrative reliability report (for the Methods section)
├── taxonomy/
│   └── indicator_taxonomy.md          ← the six indicators, theory grounding, definitions
└── code/
    ├── 01_build_pool.py               ← standardize + relevance-filter the source datasets
    └── 02_active_learning_mining.py   ← per-class ranker used to mine rare-indicator candidates
```

---

## The dataset (`data/roman_urdu_indicators_v1.csv`)

- **1,520 posts**, each labeled for six binary indicators (multi-label).
- Columns: `tweet_id`, `text`, `ig_outgroup`, `dehumanization`, `grievance`,
  `glorification`, `mobilization`, `threat`, `violence_dehum` (derived: glorification OR
  dehumanization), `split`, `source`.
- **Label policy:** double-annotated portions use **high-confidence (both-annotators-agree)**
  labels; the full-run IAA subset was adjudicated. `source` records how each row was labeled.
- **Provenance of text:** re-labeled from two public Roman Urdu corpora — **RUHSOLD**
  (haroonshakeel/roman_urdu_hate_speech) and **RU-HSD-30K** (Bilal4209/RU-HSD-30K). Original
  hate-speech labels are *not* reproduced here; only the new indicator labels. Users who want
  the raw text under the source licenses should obtain it from those repositories.

**Label distribution** (see `data/label_distribution.csv`):

| Indicator | Positives | Prevalence | Modeling status |
|---|---|---|---|
| ig_outgroup | 199 | 13.1% | trained detector |
| grievance | 78 | 5.1% | trained detector |
| mobilization | 60 | 3.9% | trained detector |
| threat | 39 | 2.6% | trained detector (lower-resourced) |
| dehumanization | 30 | 2.0% | trained detector (lower-resourced) |
| glorification | 10 | 0.7% | **descriptive only** — too rare to train |

---

## How this corpus was built (provenance summary)

1. **Source pooling & relevance filter** — RUHSOLD + RU-HSD-30K standardized into one schema,
   deduplicated to **39,458** posts; a keyword filter mapped to the six indicators isolated a
   candidate pool. (`code/01_build_pool.py`)
2. **Guideline development** — a taxonomy and annotation manual (v1.0) were piloted on 100
   posts (2 independent annotators), refined to **v1.1** via a 50-post calibration round, and
   finalized as **v1.1 FINAL** (rulings R1–R3, R6 + a threat clarification). (`guidelines/`)
3. **Full annotation run** — 1,000 posts labeled; a 350-post subset double-annotated for the
   canonical IAA (pooled Krippendorff **α = 0.96**) and adjudicated.
4. **Active-learning mining** — per-class rankers (trained on the labels) surfaced enriched
   candidates for the rare indicators; a further 520 mined posts were annotated.
   (`code/02_active_learning_mining.py`)
5. **Quality control** — one solo batch showed annotator drift (over-marking); it was caught
   by an independence/agreement check and corrected via a targeted re-label. Final labels use
   the both-agree policy throughout.

Full reliability numbers are in `agreement/IAA_REPORT.md`.

---

## Key findings this resource supports

- **A validated six-indicator taxonomy** is reliably annotatable in code-mixed Roman Urdu
  (canonical pooled α = 0.96).
- **The indicators are distinct from generic hate speech** — grievance, mobilization, and
  in/out-group framing capture content the source datasets' hate-speech labels do not.
- **A documented data ceiling:** existing public Roman Urdu hate-speech corpora contain very
  little clean, agreement-able *glorification of non-state violence* — a citable gap and a
  call for purpose-built extremism datasets in this language.

---

## Ethics & intended use

Aggregate, discourse-level research only. Do not use to profile, identify, or take action
against individuals. The text originates from public posts; user identifiers are not included.
Redistribution of the underlying text is governed by the source datasets' licenses.

## Suggested citation

*(fill in on acceptance)* — cite the article and this resource together.

## Status

Annotation and resource construction are **complete**. Next step in the project is
**detector training** (five indicators via multilingual transformer fine-tuning; glorification
reported descriptively). This folder is the frozen input to that stage and the released
artifact for the paper.

---


## Reconstructing the text (re-hydration)

This repository releases **labels only** — it does **not** redistribute the
source post text. Each row is keyed by `tweet_id = 'ru' + md5(normalized_text)[:10]`.
To attach text:

1. Obtain the two public source datasets under their own terms:
   - **RUHSOLD** (Rizwan et al., EMNLP 2020) — `task_1_*.tsv`, `task_2_*.tsv`
   - **RU-HSD-30K** (Bilal) — https://github.com/Bilal4209/RU-HSD-30K
2. Place them under `RUHSOLD/` and `RUHSD30K/`.
3. Run:
   ```
   python code/rehydrate.py \
       --ruhsold_dir RUHSOLD \
       --ru30k_csv "RUHSD30K/final 30,000 dataset_romanurdu.csv" \
       --labels data/roman_urdu_indicators_v1.csv \
       --out roman_urdu_indicators_v1_TEXT.csv
   ```
This recomputes the identifiers from the sources and joins the released labels
back to the text locally, so no source text is ever redistributed here.

## License

- **Code** (`code/`): MIT License — see `LICENSE`.
- **Data, figures, taxonomy, guidelines, agreement outputs**: CC BY 4.0 — see `LICENSE-DATA`.
- **No source post text is redistributed.** This release is labels-only, keyed by hashed IDs;
  reconstruct text locally with `code/rehydrate.py` (see above). The underlying corpora
  (RUHSOLD, RU-HSD-30K) remain under their own terms. See `LICENSE-DATA`.

## Citing this repository

See `CITATION.md` for the article citation and BibTeX. GitHub will also show a
"Cite this repository" button generated from `CITATION.cff`. After you archive a
release on Zenodo, add the resulting DOI badge to the top of this README.

## LLM evaluation (Section 7)

`llm_evaluation/` contains the prompted-LLM annotation study: per-post
predictions from Qwen2.5-7B-Instruct and Llama-3.1-8B-Instruct across three
prompting conditions, evaluated on the same held-out test fold as the
supervised detectors. See `llm_evaluation/README.md` for design and results.

Reproduce the scoring without a GPU:

```bash
python code/06_llm_annotation.py --evaluate
```

