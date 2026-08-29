# Discourse-Indicator Taxonomy

Six discourse indicators associated with violent-radicalization language, each grounded in
radicalization theory and operationalized as a binary, multi-label annotation target. The
indicators describe *how a post is worded*, not the author. Full annotation rules, boundary
cases, and Roman Urdu examples are in `../guidelines/annotation_guidelines_v1_1_FINAL.md`.

Theoretical anchors: McCauley & Moskalenko's two-pyramids (opinion vs. action radicalization);
Moghaddam's staircase to terrorism (grievance/perceived injustice as the ground floor);
Kruglanski et al.'s "3N" model (needs, narratives, networks); and the extremism-NLP literature
on framing, dehumanization, and mobilization.

| # | Indicator | Definition (short) | Theory anchor |
|---|---|---|---|
| 1 | **ig_outgroup** | Divides the world into a virtuous "us" and an opposed, illegitimate "them" framed as in conflict. | Group identity / in-group–out-group dynamics |
| 2 | **dehumanization** | Denies human/moral status to a **group** (vermin, subhuman, evil-by-nature). | Moral disengagement; precursor to intergroup violence |
| 3 | **grievance** | The in-group, or a group the author identifies with, is framed as oppressed/wronged/denied justice (incl. solidarity grievance). | Perceived injustice (staircase ground floor); "needs" |
| 4 | **glorification** | Praises or justifies **non-state / sectarian / militant** violence or its actors (martyrdom/heroism framing). | Narratives legitimizing violence |
| 5 | **mobilization** | The post itself urges the audience to take/join contentious collective action. | Action pyramid; behavioral radicalization |
| 6 | **threat** | Explicit threat, warning of harm, or stated intent to harm a target (beyond grievance/disagreement). | Escalation toward violent action |

## Design principles

- **Discourse markers, not people.** Every indicator is a property of text, scored per post.
- **Distinct from hate speech.** Grievance, mobilization, and in/out-group framing are often
  *not* hate speech; capturing them is a core purpose of the taxonomy and what distinguishes
  it from existing Roman Urdu hate-speech schemes.
- **Multi-label.** A post may carry several indicators (e.g., "come out and punish them" =
  mobilization + threat).
- **Bounded scope decisions** (finalized during guideline development):
  - *Insult vs. dehumanization (R1):* a one-off animal insult at one person is an insult;
    dehumanization requires casting a **group** as subhuman.
  - *Report vs. call (R2):* describing a protest ≠ mobilization; only a direct call to act.
  - *Solidarity grievance (R3 = yes):* grievance for a group the author identifies with counts;
    bare news reporting of others' suffering does not.
  - *Glorification scope (R6 = restrict):* non-state/sectarian/militant violence only;
    patriotic commemoration of the state armed forces is out of scope.

## Modeling status (data-driven, see IAA report)

- **Trained detectors:** ig_outgroup, grievance, mobilization, threat, dehumanization
  (the last two lower-resourced; report with confidence intervals).
- **Descriptive only:** glorification — too rare and too low-agreement in available Roman Urdu
  corpora to train a reliable classifier; its scarcity is reported as a finding.
