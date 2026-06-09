# Email -> Code Traceability 
The goal of this study is to evaluate how effectively LLMs can map developer email threads to relevant source-code components using different input representations. This project explores how LLMs can map developer email discussions to relevant system components. 

The approach uses:
- `input`: developer email threads
- `output`: source-code component
- `method`: LLM
- `comparison`: different input representations

# Research Questions
- RQ1: How accurately can LLMs map developer email threads to relevant source-code components? (exact match accuracy, relaxed match accuracy, wrong predictions, `NONE` predictions)
- RQ2: How does the input representation of developer email threads affect LLM-based component prediction? (full email thread, summary + clues, structured extraction)
- RQ3: What types of errors occur when LLMs incorrectly map email threads to source-code components? (parent component, child component, sibling component, wrong subsystem, `NONE`, keyword-based wrong match)

# Input Cases

| Case | Input Representation | Description |
|------|----------------------|-------------|
| case1 | Full Email Thread (Full subject, messages, replies, and discussion content) | Entire email thread is provided as model input |
| case2 | Summary (Short technical summary of the email thread) + Clues (Important terms, APIs, errors, files, subsystems, labels, or concepts) | Condensed summary and extracted clues are provided as model input |


## Prompt Variants

In these prompts the whole component is given as a whole and asked LLM to select most relevant component. Prompt variants differ by `only one feature at a time`. The following prompt versions are used for experimentation:

| Prompt ID | Interpret Components | Decision Rules | NONE Rule | Evidence Extraction | Change Tested |
|----------|---------------------|----------------|-----------|--------------------|-------------------------------|
| P0 | ✓ | ✓ | ✓ | ✗ | Full Detailed prompt |
| P1 | ✗ | ✓ | ✓ | ✗ | Remove interpretation section |
| P2 | ✓ | ✗ | ✓ | ✗ | Remove decision rules section |
| P3 | ✓ | ✓ | ✓ | ✓ | Add Ambiguity Check section |

## Experimental Conditions

| Condition | Input Case | Prompt |
|----------|-------------|--------|
| P0 | case1 | Control |
| P1 | case1 | No interpretation |
| P2 | case1 | No decision rules |
| P3 | case1 | Ambiguity Check |
| P0 | case2 | Control |
| P1 | case2 | No interpretation |
| P2 | case2 | No decision rules |
| P3 | case2 | Ambiguity Check |


## Task

Each prompt asks the model to:

- Read an email thread
- Compare it with components list
- Select exactly one 'component_path' or return "NONE"


## Output Format

All prompts enforce strict JSON output:
```json
{
  "component_path": "",
  "confidence": 0.0,
  "rationale": ""
}
```

## Evaluation

Results are analyzed at different levels.

### 1. Prompt Variant Comparison (Within-Case)

Prompt variants (P0–P4) are compared within each input case to assess prompt sensitivity.

Metrics:
- Prediction agreement across prompts
- Pairwise agreement between prompts
- Number of unique predictions per thread
- Frequency of `NONE` predictions
- Identification of unstable threads (unique predictions on each email_thread)


### 2. Case Comparison (Case 1 vs Case 2)

Predictions from direct full-thread mapping and sequential summary+clues mapping are compared for the same prompt variants.

Metrics:
- Cross-case agreement rate
- Cross-case prediction differences
- `NONE` prediction frequency by case
