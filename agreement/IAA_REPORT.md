# Inter-Annotator Agreement Report

Agreement was measured with **Krippendorff's α** (nominal) per indicator, on
double-annotated subsets by two independent annotators. Percent agreement is reported
alongside α because chance-corrected coefficients are unstable for low-prevalence categories
at small sample sizes (the prevalence paradox): a category can show 95%+ raw agreement yet a
low α when positives are rare. Per-round values are in `iaa_by_round.csv`.

## Canonical agreement (report this as the headline)

The **full annotation run** included a **350-post double-annotated subset** labeled under the
final guideline (v1.1 FINAL). Independence was verified (no copy fingerprint; disagreements
spread across all indicators). This is the canonical reliability estimate for the corpus:

| Indicator | Krippendorff's α |
|---|---|
| ig_outgroup | 0.987 |
| grievance | 0.978 |
| mobilization | 0.926 |
| dehumanization | 0.908 |
| threat | 0.908 |
| glorification | 0.888 |
| **Pooled (6)** | **0.963** |

## Guideline development trajectory

Agreement improved as the guideline was refined, which the paper can report as evidence of a
principled, iterative annotation protocol:

- **Pilot (100 posts, v1.0):** pooled α ≈ 0.79. Strong on ig_outgroup (0.90) and threat (0.88);
  weaker on dehumanization (0.64) and mobilization (0.58); grievance 0.79.
- **Calibration (50 posts, v1.1):** boundary rules sharpened — R1 (insult vs. dehumanization),
  R2 (reporting vs. calling in mobilization), R3 (solidarity grievance), R6 (glorification
  scope), plus a threat clarification. Rare-indicator α values here are dominated by base-rate
  noise (1–4 positives).
- **Full run (350, v1.1 FINAL):** pooled α = 0.96 (table above).

## Harder subsets (mined and solo batches)

Active-learning-mined batches concentrate difficult, near-boundary cases, so agreement is
expected to be lower there than on the canonical subset:

- **Mining subset (320):** threat 0.89 and ig_outgroup 0.89 held; grievance 0.53 and
  mobilization 0.63; **dehumanization 0.19 and glorification 0.24** — both rare *and*
  low-agreement on hard cases (annotators agreed on only one positive each). This is the
  primary evidence for the glorification data ceiling.
- **Solo-2 (200), re-labeled:** an initial pass showed annotator drift (systematic
  over-marking of ig_outgroup and grievance; pooled α ≈ 0.14). It was detected by an
  independence check, corrected with a targeted refresher note, and re-labeled — recovering to
  pooled α = 0.67 (ig_outgroup 0.80, threat 0.76, dehumanization 0.66, mobilization 0.64).
  Grievance remained divergent on this batch (0.28) but is well-supplied elsewhere. Final
  labels use the both-agree policy, which is robust to the residual disagreement.

## How labels were finalized

- **Full-run IAA subset (350):** disagreements adjudicated against the guideline.
- **All other double-annotated batches:** **both-agree (intersection)** labels — a
  high-precision policy that is robust to single-annotator drift.
- **Single-annotated solo halves:** that annotator's labels stand.

## Reporting guidance for the paper

Report the **canonical pooled α = 0.96** and the per-indicator table as the reliability of the
corpus. Report the **development trajectory** (0.79 → 0.96) as evidence of protocol quality.
Report the **mined-subset drop for glorification/dehumanization** honestly, as the basis for
treating glorification descriptively and dehumanization as lower-resourced. When reporting
detector performance, use **bootstrap confidence intervals**, since positives range from 30 to
199 across indicators.
