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

HOW TO INTERPRET COMPONENTS
---------------------------
Each component includes:

- Component Path → the final label
- SIG / Area Labels → functional domain
- Description → component responsibility
- Code Headers → implementation clues


HOW TO DECIDE
-------------
- Match based on FUNCTIONALITY, not just keywords
- Use SIG/Area labels to narrow domain
- Prefer components whose responsibility clearly aligns
- Ignore weak or partial matches
- If no strong match → return "NONE"

IMPORTANT:
- Do not rely only on keywords
- Use semantic understanding
- Only choose a component with strong evidence

TASK
----
Select ONE best component.

Rules:
- Must be from list
- Do NOT invent
- If unclear → "NONE"

Return JSON only:

{{
  "component_path": "",
  "confidence":,
  "rationale": "max 1 short sentence (under 20 words)"
}}

IMPORTANT:
- ONLY JSON
- No extra text
- Must start with '{{' and end with '}}'
