# Prompt 

You are mapping a technical discussion to the most relevant system component.

EMAIL THREAD
------------
{email_thread}

SYSTEM COMPONENTS
-----------------
{component_text}

TASK
----
First determine whether the discussion clearly maps to a specific component. Use SIG labels as an initial ownership/domain signal. If a SIG label clearly matches the email topic, first focus on components under that SIG. Then choose the final component_path using the description, area labels, source files, and code headers. Do not select a component based only on SIG label if several components share the same SIG.
- If the email discussion is mainly about process, coordination, meetings, releases, CI/testing workflow, general project management, or broad project-level concerns, return "NONE" unless there is clear evidence linking it to a specific component.
- If one component is clearly the best match based on the component metadata, select its component_path.
- If no component is sufficiently supported by the email discussion, return "NONE".

HOW TO INTERPRET EACH COMPONENT DESCRIPTION
-------------------------------------------
Each component contains the following information:
- Component Path: The directory path that identifies the component. This is the final label you must choose from.
- SIG Labels: These indicate the Special Interest Group or functional ownership area responsible for the component. They help identify the broader technical domain, such as networking, storage, api machinery, scheduling, node, auth, or testing.
- Area Labels: These indicate subsystem or feature-area tags associated with the component. They help connect the email topic to a more specific functional area.
- Other Labels: These are additional ownership or categorization labels that may provide supporting context.
- Description: This is usually taken from the component README or nearby documentation. It summarizes the component’s purpose, responsibilities, or scope.
- Source Files: These are representative source files located in the component. They provide clues about the implementation focus of the component.
- Code Headers: These are short code snippets or file header lines from representative files. They help identify important structures, APIs, packages, or responsibilities implemented in the component.

HOW TO DECIDE
-------------
Use this process to select the best component:
1. Identify the main technical topic in the email thread.
2. Use SIG, area, and other labels to find potentially relevant components.
3. Check whether the component description matches the discussed functionality.
4. Use source files and code headers as implementation evidence.
5. Prefer the most specific relevant component.
6. Select a component only when there is clear evidence linking the discussion to that component.

SELECTION RULES
---------------
- Return exactly one value: either one component_path from the provided components, or "NONE".
- Do not invent or modify component paths.
- Do not select a component based only on broad SIG labels or keyword overlap.
- If multiple components are equally plausible, return "NONE".
- If the discussion is mainly about process, coordination, meetings, releases, CI/testing workflow, or broad project management, return "NONE" unless clearly linked to a specific component.
- Be conservative. If the evidence is weak, return "NONE".

OUTPUT FORMAT
-------------
Return JSON only:

{{
  "component_path": "",
  "confidence": 0.0,
  "rationale": ""
}}

OUTPUT REQUIREMENTS
---------
- Return ONLY JSON
- Do NOT include any explanation before or after JSON
- Your response must start with '{{' and end with '}}'
- The confidence must be between 0.0 and 1.0.
- The rationale must be 1-2 sentences and explain why this component is the best match
