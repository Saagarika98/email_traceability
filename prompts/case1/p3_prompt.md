# Prompt 

You are mapping a technical discussion to the most relevant system component.

EMAIL THREAD
------------
{email_thread}

SYSTEM COMPONENTS
-----------------
{component_text}

HOW TO INTERPRET EACH COMPONENT DESCRIPTION
-------------------------------------------
Each component contains the following information:

- Component Path:
  The directory path that identifies the component. This is the final label you must choose from.

- SIG Labels:
  These indicate the Special Interest Group or functional ownership area responsible for the component.
  They help identify the broader technical domain, such as networking, storage, api machinery, scheduling, node, auth, or testing.

- Area Labels:
  These indicate subsystem or feature-area tags associated with the component.
  They help connect the email topic to a more specific functional area.

- Other Labels:
  These are additional ownership or categorization labels that may provide supporting context.

- Description:
  This is usually taken from the component README or nearby documentation.
  It summarizes the component’s purpose, responsibilities, or scope.

- Source Files:
  These are representative source files located in the component.
  They provide clues about the implementation focus of the component.

- Code Headers:
  These are short code snippets or file header lines from representative files.
  They help identify important structures, APIs, packages, or responsibilities implemented in the component.

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

TASK
----
First determine whether the discussion clearly maps to a specific component.

- If YES → select the ONE most relevant component_path
- If NO → return "NONE"

Rules:
- Return exactly ONE component_path from the provided components
- Do NOT invent component names
- Do NOT modify component names
- Prefer semantic relevance over surface keyword overlap
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
