# Detector Error Analysis (§7.1 / Discussion)

Qualitative analysis of test-set errors (baseline detector; XLM-R shows the same patterns).
Content warning: examples describe hostile/violent discourse; they are paraphrased or truncated.

## Detector comparison (context)
On AUC-PR the char-ngram TF-IDF+LR baseline beats fine-tuned XLM-RoBERTa on all five indicators
(macro 0.37 vs 0.26); F1 is mixed and confidence intervals overlap heavily. A properly-trained
multilingual transformer does **not** outperform a simple lexical baseline in this low-resource
setting — model complexity is not justified by 30–200 positives per class.

## Failure modes (test set, per indicator false negatives / false positives)

| Indicator | FN | FP | dominant error |
|---|---|---|---|
| ig_outgroup | 14 | 30 | over-fires on group-name lexicon; misses *implicit* framing in political attacks |
| grievance | 8 | 7 | misses grievance expressed via sarcasm or revenge framing |
| mobilization | 6 | 2 | misses indirect calls embedded in long complaint text |
| threat | 7 | 3 | misses metaphorical/short threats ("a crushing response is due") |
| dehumanization | 1 | **56** | fires on any animal-insult token; cannot learn the insult-vs-group-dehumanization boundary |

## Four patterns

1. **Lexical over-reliance (false positives).** Detectors key on surface hostile/group tokens
   rather than the construct. Dehumanization is the extreme case: 56 false positives because the
   model flags any post containing an animal-insult word ("kutta"), exactly the
   insult-vs-group-dehumanization distinction (rule R1) that human annotators apply but the model
   cannot learn from ~20 positives.

2. **Implicit / pragmatic expression (false negatives).** Grievance via sarcasm ("nothing will
   happen, just condemnations" = implicit grievance about impunity), mobilization embedded in
   long complaints, and metaphorical threats are missed. The models require explicit markers;
   the humans read pragmatics.

3. **Multi-label overlap is the hard zone.** Errors concentrate on posts carrying several
   indicators at once (threat + mobilization + dehumanization together), where the models
   conflate adjacent categories.

4. **Rare-class instability.** The lowest-resourced indicator (dehumanization) has catastrophic
   precision, confirming that 20–40 positives is insufficient for reliable automated detection.

## Why this strengthens the paper
The errors fall exactly where the indicators require *contextual/pragmatic judgment* — the
insult-vs-dehumanization boundary, implicit grievance, sarcastic mobilization. These are the
distinctions the validated human taxonomy encodes and that lexical or transformer models cannot
yet recover from limited data. This (a) explains the modest detector scores honestly, (b)
justifies why simple baselines remain competitive (much of the learnable signal is lexical), and
(c) frames automated detection as a starting point built on the human-validated resource, not a
solved task. File: `detector_comparison.csv`.
