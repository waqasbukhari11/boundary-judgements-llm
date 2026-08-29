# Distinctiveness from Hate Speech (§7.2)

Central claim: the indicator taxonomy captures discourse that hate-speech detection does not.
Two complementary results.

## Result A — coverage: indicators occur in non-hate discourse
Share of each indicator's positives that were **not** flagged hate/offensive in the source
datasets (a hate filter would silently drop these):

| Indicator | positives | % not hate-speech |
|---|---|---|
| glorification | 10 | 30% |
| grievance | 78 | 27% |
| mobilization | 60 | 20% |
| ig_outgroup | 199 | 17% |
| threat | 39 | 5% |
| dehumanization | 30 | 0% |

## Result B — substitution test: can a hate model do the indicator job?
A **strong** hate-speech classifier (test-set F1 = 0.865, AUC = 0.896) was used as a proxy for
each indicator and compared to the dedicated detector, on the same test fold:

| Indicator | hate-as-proxy AUC-PR | dedicated AUC-PR | ratio |
|---|---|---|---|
| grievance | 0.053 | 0.429 | 8.1× |
| mobilization | 0.062 | 0.441 | 7.1× |
| threat | 0.072 | 0.315 | 4.4× |
| ig_outgroup | 0.198 | 0.532 | 2.7× |
| dehumanization | 0.081 | 0.142 | 1.8× |

## Reading
A competent hate-speech model provides **almost no signal** for grievance and mobilization
(AUC-PR ≈ base rate) — it is effectively blind to them. The gain from a dedicated detector is
largest exactly for the indicators that Result A shows are least hate-like (grievance,
mobilization), and smallest for dehumanization, which genuinely overlaps with hate speech.
This internal consistency is the core evidence that the taxonomy is **not** a relabeling of
hate speech: it isolates grievance, mobilization, and framing that hate-speech detection cannot
recover.

Files: `distinctiveness.csv`, `hate_comparator.csv`.
