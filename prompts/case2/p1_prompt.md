# Prompt 

You are mapping a technical discussion to the most relevant system component.

SUMMARY
-------
{summary}

CLUES
-----
{clues}

SYSTEM COMPONENTS
-----------------
{component_text}

HOW TO DECIDE
-------------
To identify the best component, compare the summary and clues with the component information using these signals:

1. Main topic match
   Identify the main technical topic in the email thread.

2. Functional ownership match
   Check whether SIG Labels, Area Labels, or Other Labels align with the email topic.

3. Responsibility match
   Check whether the Description explains functionality related to the discussion.

4. Implementation clue match
   Use Source Files and Code Headers to verify whether the component likely implements the discussed topic.

5. Specificity
   Prefer the most specific relevant component over a broader or generic one.

6. Before selecting a component, ask: "Is there clear evidence that this discussion belongs to a specific component?"
      If the answer is NO, return "NONE".

TASK
----
First determine whether the discussion clearly maps to a specific component. Use SIG labels as an initial ownership/domain signal. If a SIG label clearly matches the email topic, first focus on components under that SIG. Then choose the final component_path using the description, area labels, source files, and code headers. Do not select a component based only on SIG label if several components share the same SIG.

- If the email discussion is mainly about process, coordination, meetings, releases, CI/testing workflow, general project management, or broad project-level concerns, return "NONE" unless there is clear evidence linking it to a specific component.
- If one component is clearly the best match based on the component metadata, select its component_path.
- If no component is sufficiently supported by the email discussion, return "NONE".


Rules:
- Return exactly ONE component_path from the provided components
- Do NOT invent component names
- Do NOT modify component names
- Return exactly ONE value: one component_path from the provided components, or "NONE" if no component is sufficiently supported.
- If multiple components seem equally plausible and there is no clear best match, return "NONE".
- Do not choose the closest-looking component only because of keyword overlap.
- Return "NONE" when the evidence is broad, weak, or not tied to a specific component's responsibility, source files, or code headers.
- Prefer semantic relevance over surface keyword overlap
- Be conservative: do not force a match when the evidence is weak
- If a component is selected, the selected component_path must exactly match one component_path from the provided list. Otherwise, return "NONE".

Return JSON only:

{{
  "component_path": "",
  "confidence": 0.0,
  "rationale": ""
}}

IMPORTANT:
- Return ONLY JSON
- Do NOT include any explanation before or after JSON
- Your response must start with '{{' and end with '}}'
- The rationale must be 1-2 sentences and explain why this component is the best match
