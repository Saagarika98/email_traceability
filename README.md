# Email -> Code Traceability 
This project explores how LLMs can map developer email discussions to relevant system components. 

The approach uses:
- Developer email threads
- Structured component descriptions
- Prompt-based LLM reasoning

# Input Cases

| Case | Input Representation | Description |
|------|----------------------|-------------|
| case1 | Full Email Thread | Entire email thread is provided as model input |
| case2 | Summary + Clues | Condensed summary and extracted clues are provided as model input |


## Prompt Variants

In these prompts the whole component is given as a whole and asked LLM to select most relevant component. Prompt variants differ by `only one feature at a time`. The following prompt versions are used for experimentation:

| Prompt ID | Interpret Components | Decision Rules | NONE Rule | Evidence Extraction | Change Tested |
|----------|---------------------|----------------|-----------|--------------------|-------------------------------|
| P0 | ✓ | ✓ | ✓ | ✗ | Full Detailed prompt |
| P1 | ✗ | ✓ | ✓ | ✗ | Remove interpretation section |
| P2 | ✓ | ✗ | ✓ | ✗ | Remove decision rules section |
| P3 | ✓ | ✓ | ✗ | ✗ | Remove NONE rule |
| P4 | ✓ | ✓ | ✓ | ✓ | Add evidence extraction section |

## Experimental Conditions

| Condition | Input Case | Prompt |
|----------|-------------|--------|
| C1-P0 | Full Email | Control |
| C1-P1 | Full Email | No interpretation |
| C1-P2 | Full Email | No decision rules |
| C1-P3 | Full Email | No NONE rule |
| C1-P4 | Full Email | + Evidence extraction |
| C2-P0 | Summary+Clues | Control |
| C2-P1 | Summary+Clues | No interpretation |
| C2-P2 | Summary+Clues | No decision rules |
| C2-P3 | Summary+Clues | No NONE rule |
| C2-P4 | Summary+Clues | + Evidence extraction |


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