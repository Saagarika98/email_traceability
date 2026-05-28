# Prompt 

You are mapping a technical discussion to the most relevant system component.

EMAIL THREAD
------------
{email_thread}

SYSTEM COMPONENTS
-----------------
{component_text}

HOW TO DECIDE
-------------
To identify the best component, compare the email thread with the component information using these signals:

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
First determine whether the discussion clearly maps to a specific component.

- If YES → select the ONE most relevant component_path
- If NO → return "NONE"

Rules:
- Return exactly ONE component_path from the provided components
- Do NOT invent component names
- Do NOT modify component names
- If no component matches clearly, return "NONE"
- If no component matches with clear and direct evidence, return "NONE"
- If multiple components seem similarly plausible, return "NONE"
- Prefer semantic relevance over surface keyword overlap
- Be conservative: do not force a match when the evidence is weak
- The selected component_path must exactly match one component_path from the provided list

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
