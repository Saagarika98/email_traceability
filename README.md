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
| P0 | case1 | Control |
| P1 | case1 | No interpretation |
| P2 | case1 | No decision rules |
| P3 | case1 | No NONE rule |
| P4 | case1 | + Evidence extraction |
| P0 | case2 | Control |
| P1 | case2 | No interpretation |
| P2 | case2 | No decision rules |
| P3 | case2 | No NONE rule |
| P4 | case2 | + Evidence extraction |


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