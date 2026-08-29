# Annotator Correction Note (used to fix solo-batch drift)

Issued to an annotator who over-marked `ig_outgroup` and `grievance` on a mined batch,
having drifted back toward a loose "hate-speech = positive" heuristic. Kept in the package
as provenance for the quality-control step.

**Default is 0.** Most posts carry no indicator. If more than ~a third of posts get any one
label, you're probably over-marking.

- **ig_outgroup = 1** only for a virtuous "us" vs an enemy/illegitimate "them." Criticism of a
  leader/party, or a personal insult, is **0**.
- **grievance = 1** only when a group is framed as the **victim** of injustice. Blaming or
  attacking someone, or neutral reporting, is **0**.
- **glorification = 1** only for non-state/sectarian/militant violence. State-army patriotism
  is **0**.
- **dehumanization = 1** only for a **group** cast as subhuman. A one-off animal insult at one
  person is **0**.
- **threat = 1** for a call to harm / warning of harm / revenge framing. Disagreement is **0**.
- **mobilization = 1** only for a direct call to act. Reporting a protest is **0**.

If unsure after applying the rules, mark the indicator **0** and set `uncertain = 1`.
