# Annotation Guidelines — Roman Urdu Violent-Radicalization Discourse Indicators

**Version 1.1 (FINAL) · Consolidated — supersedes v1.0 and the v1.1 addendum**

Pilot + calibration validated these rules (pilot pooled Krippendorff α ≈ 0.79). Use this single document for the full annotation run.

---

## 1. Purpose and scope
You label **discourse markers** in each post — how the text is worded. You are **not** judging whether a person is radicalized, dangerous, or guilty of anything, and never identifying individuals or intent. **Label the text, never the person.** Aggregate/population-level use only.

If a post is genuinely a specific, imminent threat to a named person, flag it to the project lead separately from labeling.

## 2. Unit of annotation
One post (tweet), whole, on its own. Do not look up the author or use outside knowledge. Reporting/quoting rule: §6.

## 3. Label schema
For each post, mark each indicator **present (1) / absent (0)**, independently. **Multi-label** — a post may carry several. Default is **0**; mark **1** only when the rule clearly applies.

`tweet_id` · `ig_outgroup` · `dehumanization` · `grievance` · `glorification` · `mobilization` · `threat` · `uncertain` (1 = genuinely unsure after applying rules) · `notes` (optional, hard cases only).

---

## 4. The six indicators

### 4.1 `ig_outgroup` — In-group vs out-group framing
Divides the world into a virtuous "us" and an opposed, illegitimate "them" framed as in conflict.
- **1:** us/them moral division; "real [nation/faith]" exclusion tests; labelling a named group traitor / ghaddar / enemy; an **implied** out-group ("*they* are oppressing *us*", "minorities are unsafe in [country]").
- **0:** ordinary "we/us" with no adversarial out-group (sports, family, generic pride); criticising a policy without the us/them division.
- ✔ `Asli [nation] wahi hai jo hamare saath khara ho` · `sary PDM waly ghaddar` → **1**
- ✘ `aaj hamari team jeet gayi` → **0**

### 4.2 `dehumanization` — Dehumanization / demonization
Denies human/moral status to a **group**, or frames people as vermin/subhuman in a way that invites their exclusion or harm.
- **1:** a **group** cast as insects/vermin/animals/subhuman/disease/evil-by-nature.
- **0:** a single animal slur at **one person** in a quarrel = **insult** (`teray jesay kuttey`, `IMRANA CHOOHA` → 0); cursing one historical/religious figure (unless it casts a living group as subhuman); **in-group self-defence** (`hum Shia jaahil nahi hai` → 0).
- ✔ `ye log insan nahi, keeray-makoray hain` → **1**

### 4.3 `grievance` — Grievance / perceived injustice / victimhood
The **in-group, or a group the author identifies/sympathises with**, is framed as oppressed, wronged, deprived, or denied justice. **(R3: solidarity grievance counts.)**
- **1:** collective victimhood of the in-group **or a solidarity group** the post adopts a victimhood frame for (e.g. fellow Muslims, Kashmiris).
- **0:** personal complaints; **attacking/blaming/taunting a target** without a victim frame (`PDM are traitors`, `you lost 93,000 troops` → 0); **neutral news reporting** of an event or others' suffering with no adopted victimhood/solidarity frame (`all of India is protesting the law` → 0; mark `uncertain` if borderline).
- ✔ `humare saath hamesha zulm hua, hamari awaaz koi nahi sunta` · `bharti fouj ne Kashmiriyon ko shaheed kiya` (solidarity frame) → **1**

### 4.4 `glorification` — Glorification / justification of violence
Praises, celebrates, or morally justifies **non-state / sectarian / militant** violence or its actors, incl. martyrdom/heroism framing. **(R6: scope is non-state/sectarian only.)**
- **1:** praising militant/sectarian perpetrators as heroes/martyrs; arguing such violence was right/necessary/deserved; celebrating a violent outcome.
- **0:** ordinary **patriotic commemoration of the state armed forces** (fallen soldiers, Nishan-e-Haider heroes, Kargil accounts) — **out of scope**; reporting or mourning violence without endorsing it; condemning violence.
- ✔ `jinhon ne jaan di wo asli hero hain` (militant/sectarian context) → **1**
- ✘ `Havaldar Lalak Jan Shaheed ne kaman sanbhal li` (state soldier) → **0**

### 4.5 `mobilization` — Mobilization / call to action
The post itself **urges the audience** to take or join contentious collective action.
- **1:** direct imperative/urging — "come out", "join", "we must march", "rise up", "don't stay silent" (`chup mat baitho, apne haq ke liye niklo`); a militant call to fight (`lar ao`).
- **0:** **reporting/describing** that a protest or struggle is happening (`awam saraapa ehtijaj hein`, `Dalits are fighting for rights` → 0); quoting someone's general aspiration unless clearly endorsed as a call to the reader; a rhetorical jab.

### 4.6 `threat` — Threat / escalatory hostility
Explicit threat, warning of harm, or stated intent to harm a target — beyond grievance or disagreement.
- **1:** direct **calls to harm** (`maro X ko`, `X ko khatam kar do`); **conditional warnings** of harm (`warna khatam ho jao gy`); revenge framing (`ab badla lene ka waqt hai`); "we won't spare them / watch what we do to X".
- **0:** disagreement/criticism without intent to harm; predicting bad outcomes with no in-group intent. **Edge → `uncertain`:** crude sexual insults and sarcastic death-wishes ("god take their life") — mark `uncertain` unless a clear intent to harm is present.

---

## 5. Boundary rules
1. **Grievance vs Dehumanization** — grievance = *we are wronged*; dehumanization = *they are subhuman*. Both can apply.
2. **Insult vs Dehumanization** — insult attacks a quality; dehumanization removes human/moral status (usually of a group).
3. **Grievance vs attack** — blaming/insulting a target is not grievance unless the in-group is framed as victim.
4. **Mobilization vs reporting** — a call to the audience to act = 1; describing an existing protest = 0.
5. **Mobilization/Threat/Glorification stack** — "come out and protest" = mobilization; "come out and burn their houses" = mobilization + threat (+ glorification if it celebrates the violence).
6. **Glorification scope** — non-state/sectarian/militant only; state-military patriotism = 0.

## 6. Edge cases
- **Sarcasm:** label by meaning conveyed; if unresolvable → `uncertain`.
- **Quoting/reporting others:** label present only if the poster **endorses/amplifies** the marker; clear condemnation or neutral reporting → absent (unclear → `uncertain`).
- **Rhetorical questions** carrying a marker count; genuine info questions don't.
- **Religious idiom** (dua, Inshallah) is not an indicator by itself.
- **Not relevant / spam / apolitical:** all six = 0 (common and valid).

## 7. Procedure (per post)
Read whole post → resolve code-mixing/sarcasm → mark the six independently (§4) → apply §5 → if still unsure, mark the indicator 0 and `uncertain = 1` → one-line `note` for hard cases only. Label each post on its own; don't "balance" your labels.

## 8. Quality control
Two annotators label the double-annotated IAA subset **independently, from separate blank files, no discussion**. Krippendorff's α per indicator (report percent agreement alongside — chance-corrected metrics are unstable for rare categories). Disagreements + all `uncertain` are adjudicated into the gold labels.

---
*v1.1 FINAL — validated on pilot (α ≈ 0.79) and calibration. Rulings R1 (dehumanization/insult), R2 (mobilization/report), R3 (solidarity grievance = yes), R6 (glorification = non-state/sectarian) incorporated.*
