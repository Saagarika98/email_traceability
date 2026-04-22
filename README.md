# Email -> Code Traceability 
This project explores how LLMs can map developer email discussions to relevant system components. 

The approach uses:
- Developer email threads
- Structured component descriptions
- Prompt-based LLM reasoning

## Prompt Variants

In these prompts the whole component is given as a whole and asked LLM to select most relevant component. The following prompt versions are used for experimentation:

- 'single_shot.md' 
  Baseline prompt using standard decision rules.

- 'single_shot_detailed.md'  
  There is a detailed explantion on the component description of each category and functionalities. Even for deciding the component there are some rules described. Aims to improve reasoning quality and reduce ambiguous mappings

- 'single_shot_relaxed.md' 
  Allows selection of the best available match even with partial evidence. Uses "NONE" only when no reasonable mapping exists. Reduces "NONE" predictions but may increase incorrect matches.
  
- 'single_shot_strict.md'  
  Requires clear and direct evidence before selecting a component. Reduces false positives but may increase "NONE" predictions. 
  Encourages returning "NONE" when:
    - multiple components are plausible
    - evidence is incomplete or indirect

## Task

Each prompt asks the model to:

- Read an email thread
- Compare it with components list
- Select exactly one 'component_path' or return "NONE"


## Output Format

All prompts enforce strict JSON output:

{
  "component_path": "",
  "confidence": 0.0,
  "rationale": ""
}