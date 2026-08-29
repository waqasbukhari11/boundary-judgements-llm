# Cross-Source Generalization (§7.1 robustness)

Addresses the objection that detectors memorize one dataset's style. The corpus draws from two
stylistically distinct sources: RU-HSD-30K (political, 1,214 posts) and RUHSOLD (interpersonal
abuse, 306 posts). We train on one source and test on the fully held-out other. Because RUHSOLD
is small and sparse in most indicators, only the direction **train RU-HSD-30K → test RUHSOLD**
is feasible, and only indicators with enough held-out positives are testable.

| Indicator | held-out test positives | cross-source AUC-PR | base rate | in-domain AUC-PR |
|---|---|---|---|---|
| ig_outgroup | 34 | **0.605** | 0.111 | 0.532 |
| mobilization | 14 | 0.110 | 0.046 | 0.441 |
| grievance | 6 | 0.215 | 0.020 | 0.429 (too few — weak) |
| threat | 4 | 0.160 | 0.013 | 0.315 (too few — weak) |
| dehumanization | 1 | — | — | (untestable) |

## Reading
- **ig_outgroup generalizes strongly**: trained only on the political source, it detects in/out-
  group framing in the unseen abuse source at AUC-PR 0.61 — above its in-domain score and 5.5×
  base rate. Clear evidence the detector captures the construct, not source-specific style.
- **mobilization** generalizes above chance (2.4× base) but degrades from in-domain — partial,
  with some source-dependence.
- **grievance/threat/dehumanization** cannot be reliably cross-source tested here (≤6 held-out
  positives). A full cross-domain evaluation for the rare indicators requires a **third,
  independently labeled Roman Urdu source** — stated as future work.

## Positioning
Report this as evidence of cross-source generalization for the frequent indicators (esp.
ig_outgroup), with the explicit limitation that rare-indicator generalization is untested and
left to future external validation. File: `cross_source.csv`.
