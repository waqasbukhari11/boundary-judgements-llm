# Indicator Co-occurrence Structure (§7.3)

The six indicators are not independent: they co-occur in theoretically-predicted ways, which is
evidence the taxonomy carves discourse at meaningful joints rather than arbitrary categories.

## Multiplicity
Of 1,520 posts, 1,203 carry no indicator, 237 carry one, 64 carry two, 16 carry three or more.
Among the 317 indicator-bearing posts, **25% carry more than one indicator** — radicalization
discourse markers frequently travel together.

## Pairwise co-occurrence (Fisher odds ratios, significant pairs, OR>1)

| Pair | P(B \| A) | OR | p |
|---|---|---|---|
| threat ↔ mobilization | 0.46 | 29.4 | <0.001 |
| dehumanization ↔ ig_outgroup | 0.63 | 12.6 | <0.001 |
| mobilization ↔ glorification | — | 10.9 | 0.006 |
| glorification ↔ ig_outgroup | — | 4.5 | 0.032 |
| threat ↔ dehumanization | — | 4.5 | 0.039 |
| ig_outgroup ↔ grievance | 0.14 | 3.9 | <0.001 |
| ig_outgroup ↔ mobilization | 0.10 | 3.6 | <0.001 |
| mobilization ↔ grievance | 0.15 | 3.6 | 0.003 |
| ig_outgroup ↔ threat | 0.06 | 2.7 | 0.013 |

## Structure (maps onto radicalization theory)
- **in/out-group framing is the hub** — it co-occurs significantly with every other indicator.
  Identity framing is the connective tissue of the discourse.
- **Identity-hostility cluster:** ig_outgroup + dehumanization (OR 12.6) — you dehumanize the
  framed out-group.
- **Action cluster:** threat + mobilization (OR 29.4) — calls to act and threats travel
  together.
- **Grievance bridges** into framing and mobilization (OR ~3.6–3.9), consistent with theory in
  which perceived injustice motivates in/out-group framing and collective action.

Empirically, the co-occurrence recovers the theorized pathway grievance → framing/dehumanization
→ mobilization/threat.

**Caveat.** Pairs involving the rare indicators (glorification, threat, dehumanization) rest on
few co-occurring posts, so those odds ratios are point estimates with wide uncertainty; the
high-frequency pairs (threat↔mobilization, dehumanization↔ig_outgroup, ig_outgroup↔grievance,
ig_outgroup↔mobilization) are the robust ones. File: `cooccurrence.csv`.
