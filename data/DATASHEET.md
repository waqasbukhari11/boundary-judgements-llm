# Datasheet — Roman Urdu Discourse-Indicator Corpus v1

Following the *Datasheets for Datasets* structure.

## Motivation
Created to enable reliable, aggregate-level study of violent-radicalization *discourse
indicators* in code-mixed Roman Urdu — a low-resource setting where prior work stops at
post-level hate-speech classification. The dataset operationalizes a theory-grounded taxonomy
so that indicator prevalence can be measured and detectors trained.

## Composition
- **Instances:** 1,520 Roman Urdu posts, each with six binary indicator labels.
- **Labels:** `ig_outgroup`, `dehumanization`, `grievance`, `glorification`, `mobilization`,
  `threat` (multi-label); plus derived `violence_dehum` = glorification OR dehumanization.
- **Positives:** ig_outgroup 199, grievance 78, mobilization 60, threat 39, dehumanization 30,
  glorification 10. 1,203 posts carry no indicator (valid, expected).
- **Splits column (`split`):** provenance of each row (full-run IAA subset, solo halves, mined
  batch, re-labeled solo batch). Not a train/test split — modeling splits are created
  downstream, stratified, with a held-out test set drawn from double-annotated rows.
- **Source text:** re-labeled from public corpora RUHSOLD and RU-HSD-30K. Original
  hate-speech labels are not redistributed here.

## Collection & labeling process
- Source datasets standardized and deduplicated (39,458 unique posts); relevance-filtered to a
  candidate pool via indicator-mapped keywords.
- Two independent annotators labeled under a manual developed through pilot (100) →
  calibration (50) → final (v1.1 FINAL). A 350-post subset was double-annotated for IAA
  (pooled Krippendorff α = 0.96) and adjudicated.
- Rare indicators were enriched via active-learning mining (per-class rankers trained on the
  labels; 520 additional posts annotated).
- **Label finalization:** adjudication on the IAA subset; **both-annotators-agree** on other
  double-annotated batches; single-annotator labels on solo halves.

## Preprocessing
Light normalization only (whitespace, control-character stripping, URL handling); Roman Urdu
spelling/transliteration variation preserved. No stemming or aggressive normalization.

## Uses
Intended: training/evaluating indicator detectors; measuring indicator prevalence; studying the
distinction between these indicators and hate speech; methodological work on low-resource
annotation. **Not** intended for profiling individuals, inferring intent, or enforcement.

## Distribution & licensing
The indicator labels (this file) accompany the article. The underlying post text is governed by
the source datasets' licenses; obtain raw text from the original RUHSOLD and RU-HSD-30K
repositories.

## Known limitations
- **glorification** is very rare (10 positives) and low-agreement on hard cases — treated as
  descriptive, not trained. **dehumanization** (30) and **threat** (39) are lower-resourced;
  detector metrics should carry bootstrap confidence intervals.
- Source corpora are hate-speech/political datasets; content richer in militant glorification is
  underrepresented (a documented data ceiling).
- Sourced from public posts in a specific sociopolitical context (Pakistan-centric Roman Urdu);
  transfer to other regions/periods is untested.

## Distribution (text handling)
This resource is distributed as **labels only**; the source post text is not
included or redistributed. Rows are keyed by `tweet_id = 'ru' + md5(normalized_text)[:10]`.
Text is reconstructed locally from the public source datasets (RUHSOLD, RU-HSD-30K)
using `code/rehydrate.py`. Illustrative examples elsewhere in the package are the
authors' own paraphrases, not verbatim posts.
