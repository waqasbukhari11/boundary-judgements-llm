# RU-RAD-6 Supplementary Materials (S1–S5)

**Boundary-Aware Natural Language Processing for Violent-Radicalization Discourse in Low-Resource Roman Urdu**

*Supplementary materials for the manuscript submitted to Scientific Reports*

Purpose. This supplementary package consolidates material that directly supports reproducibility of the manuscript: the frozen annotation instrument, prompting specification, reported bootstrap results, an extended confusion-matrix specification, and the documented error-analysis findings.

**Important reproducibility note:** No numerical result that is not reported or recoverable from the manuscript was invented in this package. Where the manuscript refers to released raw predictions or exact few-shot examples but does not print those underlying records, this document identifies them as repository-level artifacts rather than fabricating replacements.

## Contents

- [S1. Full Annotation Guideline v1.1](#s1-full-annotation-guideline-v11)
- [S2. Complete Prompting Specification and Few-Shot Package](#s2-complete-prompting-specification-and-few-shot-package)
- [S3. Per-Indicator Bootstrap Results](#s3-per-indicator-bootstrap-results)
- [S4. Extended Confusion-Matrix Supplement](#s4-extended-confusion-matrix-supplement)
- [S5. Additional Model Outputs and Error Analysis](#s5-additional-model-outputs-and-error-analysis)

## S1. Full Annotation Guideline v1.1

Version: v1.1 (frozen before final reliability measurement). Scope: Roman Urdu (Latin-script Urdu, code-mixed) social-media posts; multi-label annotation; six discourse indicators. The guideline describes the text of a post, not the person who wrote it.

### S1.1 Annotation unit and label set

Each post may receive zero, one, or several indicators. Annotators should apply the definitions to the content and stance expressed in the post, using contextual interpretation where necessary. The six valid label strings used in the computational experiments are: ig_outgroup, dehumanization, grievance, glorification, mobilization, threat.

| Indicator  | Working definition                                                                                   | Theoretical anchor                       |
|----------------|----------------------------------------------------------------------------------------------------------|----------------------------------------------|
| ig_outgroup    | Divides the world into a virtuous “us” and an opposed, illegitimate “them” framed as in conflict.        | Group identity; in-group/out-group dynamics. |
| dehumanization | A group is cast as subhuman, vermin, or evil-by-nature; distinct from an insult aimed at one person.     | Moral disengagement; precursor to violence.  |
| grievance      | The in-group, or a group the author identifies with, is framed as oppressed, wronged, or denied justice. | Perceived injustice; staircase ground floor. |
| glorification  | Praise or justification of non-state, sectarian, or militant violence or its actors.                     | Narratives legitimizing violence.            |
| mobilization   | A direct call to the audience to take or join collective, contentious action.                            | Action pyramid; behavioral radicalization.   |
| threat         | An explicit threat, warning of harm, or stated intent to harm a target.                                  | Escalation toward violent action.            |

### S1.2 Fixed boundary rules

| Rule                                        | Operational boundary                                                                                                                                                          |
|-------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| R1 — Individual insult vs. group dehumanization | An insult aimed at one person, including animal metaphors, is not dehumanization. Dehumanization requires casting a whole group as subhuman.                                      |
| R2 — Reporting action vs. mobilization          | Reporting that a protest or collective action occurred is not mobilization. Mobilization requires a direct call to the audience to take or join collective, contentious action.   |
| R3 — Target attack vs. solidarity grievance     | Grievance requires a collective victimhood frame for a group with which the author identifies. Bare reporting of another group’s suffering does not qualify.                      |
| R4 — Explicit vs. implied group opposition      | In/out-group framing can be expressed through implied as well as explicitly named oppositions; the group division must nevertheless function as an us-versus-them conflict frame. |

### S1.3 Annotation procedure

- Read the complete post before assigning any label.

- Evaluate each of the six indicators independently; multi-label assignments are allowed.

- Apply the frozen definitions and boundary rules rather than relying on isolated lexical triggers.

- Use NONE when none of the six indicators clearly applies.

- Do not infer an indicator from the identity, ideology, or presumed intentions of the author.

- When a case is genuinely ambiguous, follow the frozen boundary rule and annotation guidance rather than inventing a new rule.

- During guideline development, disagreements were resolved through pilot/calibration and adjudication; the final guideline was then frozen before the canonical reliability measurement.

### S1.4 Illustrative paraphrased patterns

| Indicator  | Paraphrased illustrative pattern                                    |
|----------------|-------------------------------------------------------------------------|
| In/out-group   | “They have always been against people like us; this is us versus them.” |
| Dehumanization | “That whole community are animals, not human beings.”                   |
| Grievance      | “Our people are wronged again and again and no one answers for it.”     |
| Glorification  | “Those who took up arms against them are heroes; their path was right.” |
| Mobilization   | “Everyone must come out together and confront them now.”                |
| Threat         | “They will be made to pay; a crushing response is coming.”              |

These are paraphrased English glosses used in the manuscript, not verbatim source posts. They are included here to avoid reproducing hostile source content while preserving the operational distinction among labels.

### S1.5 Reliability and corpus use

The canonical reliability subset contains 350 doubly annotated posts and is disjoint from guideline development. The manuscript reports pooled Krippendorff’s α = 0.963, with per-indicator agreement reported in its reliability table. The final RU-RAD-6 corpus contains 1,520 posts. The frozen guideline was also applied unchanged to the independent Twitter validation corpus.

## S2. Complete Prompting Specification and Few-Shot Package

This section reproduces the prompt structure documented in the manuscript. The manuscript states that five labelled examples were held constant across all posts and covered one empty-label case, two single-label cases, and two multi-label cases. The exact original five examples and raw responses are repository artifacts; they are not printed verbatim in the manuscript. To avoid creating a false record, this package reproduces the exact common header and condition structure and separately gives the manuscript’s paraphrased examples as a semantic reference.

### S2.1 Common instruction header

```text
You are labeling short Roman Urdu (Latin-script Urdu, code-mixed) social media posts for six discourse indicators. A post may have zero, one, or several indicators. Most posts have NONE — only label an indicator when the rule clearly applies. Return ONLY a JSON object: {"labels": [<indicator names present>]}.
```

Valid labels, in fixed order: ig_outgroup, dehumanization, grievance, glorification, mobilization, threat.

### S2.2 Zero-shot condition

```text
[COMMON INSTRUCTION HEADER]

Labels: ig_outgroup, dehumanization, grievance, glorification, mobilization, threat.

Post:
<POST TEXT>

Return ONLY the JSON object.
```

The zero-shot condition appends the post alone after the common instruction.

### S2.3 Few-shot condition

```text
[COMMON INSTRUCTION HEADER]

Labels: ig_outgroup, dehumanization, grievance, glorification, mobilization, threat.

Example 1 — EMPTY LABEL:
<held-constant labelled example 1>
Output: {"labels": []}

Example 2 — SINGLE LABEL:
<held-constant labelled example 2>
Output: {"labels": ["<indicator>"]}

Example 3 — SINGLE LABEL:
<held-constant labelled example 3>
Output: {"labels": ["<indicator>"]}

Example 4 — MULTI LABEL:
<held-constant labelled example 4>
Output: {"labels": ["<indicator>", "<indicator>"]}

Example 5 — MULTI LABEL:
<held-constant labelled example 5>
Output: {"labels": ["<indicator>", "<indicator>"]}

Post:
<POST TEXT>

Return ONLY the JSON object.
```

**Alignment note:** The manuscript does not print the literal five examples; it states their composition and says the complete examples are released in the repository. The exact five examples are provided in the repository.

### S2.4 Taxonomy/boundary condition

```text
[COMMON INSTRUCTION HEADER]

The six indicator definitions from the frozen annotation guideline are appended verbatim, including their exclusion/boundary clauses. In particular, the taxonomy condition supplies the boundary rules used by the human annotators.

Post:
<POST TEXT>

Return ONLY the JSON object.
```

No system prompt is used. The entire instruction is delivered as a single user turn through each model’s chat template.

### S2.5 Parsing and inference controls

| Setting        | Manuscript-aligned value                                                                                   |
|--------------------|----------------------------------------------------------------------------------------------------------------|
| Models             | Qwen2.5-7B-Instruct; Llama-3.1-8B-Instruct; Qwen2.5-72B-Instruct                                               |
| Decoding           | Greedy; do_sample=False; temperature=0; top-p not applied                                                      |
| Max new tokens     | 64                                                                                                             |
| Repetition penalty | Not applied; library default 1.0                                                                               |
| Quantization       | 4-bit NF4, float16 compute for 7B/8B models                                                                    |
| Inference          | 7B/8B local via HuggingFace transformers on a single NVIDIA T4; 72B hosted via HuggingFace Inference Providers |
| Output format      | JSON object {"labels": \[...\]}; malformed and refusal responses logged                                        |
| Repetitions        | Single deterministic pass                                                                                      |
| Evaluation fold    | Held-out test fold, n=227, identical across models                                                             |
| Inference date     | August 2026                                                                                                    |

Parsing: extract the first JSON object and retain recognized label strings; if no JSON object is present, apply the fallback literal-indicator scan; otherwise record the response as malformed. Refusals are tracked separately. The manuscript reports no refusals and no malformed responses in the reported runs.

## S3. Per-Indicator Bootstrap Results

The manuscript specifies 2,000 bootstrap resamples and reports per-indicator performance on the held-out test fold. Because the manuscript text available for this package contains the point estimates but not every numeric confidence-limit pair, this supplement records the exact reported point estimates and the bootstrap protocol without fabricating interval endpoints.

### S3.1 Supervised detector results

| Indicator  | Baseline F1 | XLM-R F1 | Baseline AUC-PR | XLM-R AUC-PR | MuRIL AUC-PR |
|----------------|-----------------|--------------|---------------------|------------------|------------------|
| In/out-group   | 0.23            | 0.38         | 0.53                | 0.34             | 0.48             |
| Grievance      | 0.05            | 0.28         | 0.43                | 0.33             | 0.29             |
| Mobilization   | 0.07            | 0.3          | 0.44                | 0.35             | 0.43             |
| Threat         | 0.03            | 0.25         | 0.32                | 0.46             | 0.17             |
| Dehumanization | 0.07            | 0.09         | 0.14                | 0.2              | 0.15             |
| Macro average  | 0.09            | 0.26         | 0.37                | 0.34             | 0.3              |

The manuscript identifies AUC-PR as the primary ranking metric and states that precision, recall, F1, and AUC-PR were evaluated with bootstrap 95% confidence intervals over 2,000 resamples. MuRIL F1 is not reported in the manuscript’s Table 6.

### S3.2 Taxonomy-prompt LLM results

| Indicator                    | XLM-R F1 | TF-IDF F1 | Qwen 7B F1 | Llama 8B F1 | Qwen 72B F1 | Gold positives |
|----------------------------------|--------------|---------------|----------------|-----------------|-----------------|--------------------|
| In/out-group                     | 0.381        | 0.349         | 0.233          | 0.34            | 0.476           | 34                 |
| Mobilization                     | 0.25         | 0.222         | 0.136          | 0.345           | 0.429           | 9                  |
| Grievance                        | 0.253        | 0.128         | 0.14           | 0.333           | 0.286           | 11                 |
| Threat                           | 0.271        | 0.294         | 0.435          | 0.462           | 0.167           | 8                  |
| Dehumanization                   | 0.178        | 0.107         | 0.089          | 0.2             | 0.149           | 6                  |
| Glorification                    | 0.118        | 0.114         | 0.0            | —               | —               | 2                  |
| Macro-F1 (5 modelled indicators) | 0.267        | 0.22          | 0.207          | 0.336           | 0.301           | —                  |

The test fold contains only 2 glorification positives; the manuscript explicitly treats this class as statistically underpowered for automated performance claims.

### S3.3 Paired bootstrap comparison reported in the manuscript

| Comparison              | Δ Macro-F1 (6 indicators) | 95% CI         | p |
|-----------------------------|-------------------------------|--------------------|-------|
| Qwen2.5-7B vs Llama-3.1-8B  | -0.03                         | \[-0.089, +0.028\] | 0.298 |
| Qwen2.5-7B vs Qwen2.5-72B   | -0.07                         | \[-0.132, -0.006\] | 0.033 |
| Llama-3.1-8B vs Qwen2.5-72B | -0.039                        | \[-0.104, +0.030\] | 0.29  |

These are paired percentile intervals based on 5,000 resamples of the 227-post test fold. The manuscript cautions that only one comparison excludes zero and that inference conditions differ between the hosted 72B model and the locally run smaller models.

### S3.4 Prompt-condition results for Qwen2.5-7B

| Indicator           | Zero-shot F1 | Few-shot F1 | Taxonomy F1 |
|-------------------------|------------------|-----------------|-----------------|
| In/out-group            | 0.143            | 0.293           | 0.233           |
| Dehumanization          | 0.085            | 0.13            | 0.089           |
| Grievance               | 0.126            | 0.164           | 0.14            |
| Glorification           | 0.0              | 0.0             | 0.0             |
| Mobilization            | 0.208            | 0.154           | 0.136           |
| Threat                  | 0.308            | 0.538           | 0.435           |
| Macro-F1 (6 indicators) | 0.145            | 0.213           | 0.172           |
| Predicted positives     | 298              | 217             | 244             |

The manuscript reports that the five-example few-shot condition has macro-F1 0.213, compared with 0.145 zero-shot and 0.172 taxonomy, with predicted-positive counts of 217, 298, and 244 respectively.

## S4. Extended Confusion-Matrix Supplement

The manuscript’s evaluation is multi-label and reports per-indicator F1/AUC-PR, over-production, shared false positives, and paired correctness tests. It does not print complete TP/FP/FN/TN matrices for every model-indicator combination. Therefore, the tables below are an aligned reporting framework rather than fabricated numerical matrices. Exact cell counts should be populated directly from the released model-output files.

### S4.1 Required binary confusion-matrix structure

| System      | Indicator | TP                    | FP                    | FN                    | TN                    | Support (positive) |
|-----------------|---------------|---------------------------|---------------------------|---------------------------|---------------------------|------------------------|
| TF-IDF baseline | ig_outgroup   | \[from released outputs\] | \[from released outputs\] | \[from released outputs\] | \[from released outputs\] | 34                     |
| XLM-RoBERTa     | ig_outgroup   | \[from released outputs\] | \[from released outputs\] | \[from released outputs\] | \[from released outputs\] | 34                     |
| MuRIL           | ig_outgroup   | \[from released outputs\] | \[from released outputs\] | \[from released outputs\] | \[from released outputs\] | 34                     |
| Qwen2.5-7B      | ig_outgroup   | \[from released outputs\] | \[from released outputs\] | \[from released outputs\] | \[from released outputs\] | 34                     |
| Llama-3.1-8B    | ig_outgroup   | \[from released outputs\] | \[from released outputs\] | \[from released outputs\] | \[from released outputs\] | 34                     |
| Qwen2.5-72B     | ig_outgroup   | \[from released outputs\] | \[from released outputs\] | \[from released outputs\] | \[from released outputs\] | 34                     |

Repeat the same structure for dehumanization, grievance, glorification, mobilization, and threat. The total test-fold size is n=227.

### S4.2 LLM prompt-condition matrix structure

| Qwen2.5-7B condition | Indicator      | TP                    | FP                    | FN                    | TN                    | Predicted positives |
|--------------------------|--------------------|---------------------------|---------------------------|---------------------------|---------------------------|-------------------------|
| Zero-shot                | All six indicators | \[from released outputs\] | \[from released outputs\] | \[from released outputs\] | \[from released outputs\] | 298                     |
| Few-shot                 | All six indicators | \[from released outputs\] | \[from released outputs\] | \[from released outputs\] | \[from released outputs\] | 217                     |
| Taxonomy                 | All six indicators | \[from released outputs\] | \[from released outputs\] | \[from released outputs\] | \[from released outputs\] | 244                     |

### S4.3 Shared-false-positive summary

| Error structure                                | Reported manuscript value / finding                                                                  |
|----------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Shared false positives across the two smaller LLMs | 127 inspected shared false positives                                                                     |
| Shared false positives vs true positives           | 58 shared false positives against 70 true positives                                                      |
| Supervised dehumanization error pattern            | 56 false positives against 1 false negative                                                              |
| Main dehumanization trigger pattern                | Individual-directed animal-insult vocabulary and profanity without a group reference                     |
| Main grievance trigger pattern                     | Victimhood vocabulary occurring in personal complaint, factual reporting, or ordinary political argument |
| Boundary issue implicated                          | R1 for individual insult vs group dehumanization; R3 for collective grievance vs non-grievance contexts  |

For publication-quality supplementary matrices, use the repository’s released raw predictions and gold labels to calculate each cell. This preserves exact alignment with the manuscript and avoids reconstructing counts from rounded F1 values.

## S5. Additional Model Outputs and Error Analysis

### S5.1 Model-output inventory

| Artifact                        | Scope described by manuscript                                | Status for supplement |
|-------------------------------------|------------------------------------------------------------------|---------------------------|
| Human gold labels                   | Frozen held-out test fold; n=227; adjudicated reference standard | Repository artifact       |
| Supervised detector predictions     | TF-IDF baseline, XLM-RoBERTa, MuRIL                              | Repository artifact       |
| LLM predictions                     | Qwen2.5-7B, Llama-3.1-8B, Qwen2.5-72B; taxonomy condition        | Repository artifact       |
| Prompt-condition predictions        | Qwen2.5-7B; zero-shot, few-shot, taxonomy                        | Repository artifact       |
| Raw LLM responses                   | Every reported inference response                                | Repository artifact       |
| Parser outputs                      | Recognized labels, malformed/refusal tracking                    | Repository artifact       |
| Frozen train/validation/test splits | Released for reproducibility                                     | Repository artifact       |

### S5.2 Shared failure mechanism

The manuscript identifies a common surface-trigger mechanism across automated systems. For dehumanization, the two smaller LLMs frequently responded to animal-insult vocabulary even when the text targeted a single individual rather than a group. This directly conflicts with R1, which requires group-level subhuman characterization.

For grievance, shared false positives clustered around victimhood-related vocabulary appearing in personal complaints, factual reports of others’ suffering, and ordinary political argument. R3 requires a collective victim frame with which the author identifies; lexical presence alone is insufficient.

The supervised analysis shows a related pattern: the dehumanization detector produced 56 false positives against one false negative, indicating that lexical cues can dominate even when a model is explicitly trained for the boundary-defined construct.

### S5.3 Error-analysis taxonomy

| Error class                                  | Operational description                                                                                                          | Relevant boundary               |
|--------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------|
| Lexical trigger without target qualification     | Indicator-like word or phrase occurs, but the required target/group relation is absent.                                              | R1                                  |
| Reported event mistaken for action call          | Text describes a protest or collective action without directing the audience to act.                                                 | R2                                  |
| Suffering report mistaken for grievance          | Text reports harm or injustice without adopting a collective in-group victim frame.                                                  | R3                                  |
| Implied group opposition missed or over-produced | Model fails to distinguish contextual us-versus-them framing from generic disagreement.                                              | R4                                  |
| Violence praise outside the defined scope        | Praise/commemoration is mapped to glorification despite the taxonomy’s restriction to non-state, sectarian, or militant violence.    | Glorification scope                 |
| Over-labeling under prompted LLMs                | Models produce substantially more positives than the gold reference despite explicit instructions that most posts have no indicator. | Prompt adherence / boundary control |

### S5.4 Prompt-condition error profile

| Condition | Macro-F1 (6 indicators) | Predicted positives | Manuscript interpretation                                                                          |
|---------------|-----------------------------|-------------------------|--------------------------------------------------------------------------------------------------------|
| Zero-shot     | 0.145                       | 298                     | Highest over-production among the three Qwen2.5-7B conditions.                                         |
| Few-shot      | 0.213                       | 217                     | Largest macro-F1 among the three tested prompting conditions and lower over-production than zero-shot. |
| Taxonomy      | 0.172                       | 244                     | Explicit boundary definitions improve over zero-shot but do not remove over-production.                |

### S5.5 Model-agreement outputs

| Model pair              | Cohen’s κ |
|-----------------------------|---------------|
| Qwen2.5-7B vs Llama-3.1-8B  | 0.242         |
| Qwen2.5-7B vs Qwen2.5-72B   | 0.261         |
| Llama-3.1-8B vs Qwen2.5-72B | 0.281         |

The manuscript explicitly notes that these are inter-model agreement values; direct model-human κ is not used as the principal comparison because the evaluation is against the adjudicated reference standard.

### S5.6 Raw-output file structure

- File S5.1: gold_labels_test.csv — one row per held-out post and six gold binary labels.

- File S5.2: supervised_predictions_test.csv — TF-IDF, XLM-RoBERTa, and MuRIL predictions/scores.

- File S5.3: qwen7b_prompt_outputs.csv — zero-shot, few-shot, and taxonomy outputs plus parsed labels.

- File S5.4: llama8b_taxonomy_outputs.csv — raw and parsed outputs.

- File S5.5: qwen72b_taxonomy_outputs.csv — raw and parsed outputs.

- File S5.6: error_cases.csv — model, indicator, gold label, predicted label, error type, and boundary rule.

- File S5.7: bootstrap_results.csv — metric, system, indicator, point estimate, lower CI, upper CI, number of resamples, and seed.

- File S5.8: confusion_matrices.csv — system, condition, indicator, TP, FP, FN, TN.

### S5.7 Reproducibility statement

The manuscript states that corpus labels, the frozen v1.1 guideline, taxonomy, agreement evidence, frozen splits, model outputs, prompting conditions with exact prompt text and inference settings, and evaluation code are openly released in the project repository. Source post text is not redistributed because of platform terms and source-dataset licensing; it is reconstructed locally from the public source corpora using the released script.
