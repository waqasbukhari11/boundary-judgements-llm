# ACLED External-Grounding Report (§7.4)

**Design.** Non-temporal external construct validation. The corpus is untimed, so no
predictive/temporal claim is made. We test whether indicator-bearing discourse references the
same conflict actors/themes that ACLED independently documents for Pakistan (33,898 events,
2021–2024), against a null (indicator-negative discourse), plus an indicator→cleavage mapping.

## Result 1 — Anchoring (indicator-positive vs. negative reference rates)

Indicator-positive posts reference ACLED conflict actors/themes more than negative posts:

| Indicator | ref-rate (pos) | ref-rate (neg) | lift | p |
|---|---|---|---|---|
| ig_outgroup | 0.61 | 0.28 | 2.15 | <0.001 |
| dehumanization | 0.63 | 0.32 | 1.98 | <0.001 |
| grievance | 0.60 | 0.31 | 1.94 | <0.001 |
| mobilization | 0.43 | 0.32 | 1.35 | 0.09 |
| glorification | 0.40 | 0.33 | 1.23 | 0.87 (n=10) |
| threat | 0.33 | 0.33 | 1.02 | 1.00 |

**Reading.** The identity/grievance indicators (ig_outgroup, dehumanization, grievance) are
significantly anchored in the real conflict landscape (~2×, p<0.001). Threat and mobilization
are *stance/action* markers rather than actor-naming, so a null anchoring result is expected
and interpretable, not a failure. Glorification is too rare (n=10) to test.

## Result 2 — Cleavage specificity (% of an indicator's positives referencing each cleavage)

| Indicator | militant | sectarian | ethnic | political |
|---|---|---|---|---|
| ig_outgroup | 14 | **23** | 3 | 13 |
| dehumanization | **13** | 7 | 10 | 3 |
| grievance | 8 | **18** | 4 | 12 |
| glorification | **30** | 20 | 0 | 10 |
| mobilization | 5 | 5 | 3 | **13** |
| threat | 3 | 5 | 0 | **10** |

**Reading.** The mapping is structured, not uniform: glorification→militant, ig_outgroup→
sectarian, mobilization/threat→political. This indicator-specific correspondence is genuine
construct validity and rebuts the "both merely mention politics" objection. Notably,
glorification maps most to the *militant* cleavage — external evidence that the label captures
the non-state/militant content its scope (R6) intended, even though it is too rare to train.

## Honest positioning
This is thematic **construct validity**, not temporal prediction or causation. It supports the
claim that the indicators reflect real conflict structure; it does not claim discourse predicts
events. Report it as external validity supporting the taxonomy — not as the paper's headline.
Files: `acled_grounding_results.csv`, `acled_cleavage_specificity.csv`, `acled_reference_gazetteer.csv`.

## Result 1b — hardened anchoring (odds ratios + permutation test)

Using a **fixed, ACLED-derived gazetteer** (126 terms built reproducibly from actor/region
fields; reported in `acled_reference_gazetteer.csv`), with Fisher odds ratios (Woolf 95% CI)
and a 5,000-iteration label-permutation test on the lift:

| Indicator | OR | 95% CI | perm p | verdict |
|---|---|---|---|---|
| ig_outgroup | 3.93 | [2.89, 5.34] | 0.0002 | robust |
| dehumanization | 3.68 | [1.76, 7.69] | 0.0006 | robust |
| grievance | 3.36 | [2.12, 5.35] | 0.0002 | robust |
| mobilization | 1.62 | [0.96, 2.71] | 0.054 | fragile |
| glorification | 1.38 | [0.41, 4.62] | 0.42 | null (n=10) |
| threat | 1.04 | [0.53, 2.01] | 0.51 | null |

**Robustly anchored:** ig_outgroup, dehumanization, grievance — OR CIs exclude 1 and the
anchoring survives permutation (p<0.001). Mobilization is borderline; threat and glorification
are null (threat = stance not actor-naming; glorification underpowered at n=10).

**Reproducibility note.** The result is sensitive to the gazetteer, so the gazetteer is fixed
and derived deterministically from the ACLED export (`code/05_acled_grounding.py`); it is
released with the resource. Report the three robust indicators as the grounding claim; do not
claim mobilization/threat/glorification anchoring. File: `acled_grounding_hardened.csv`.
