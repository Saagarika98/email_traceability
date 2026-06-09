import json
import os
import re
from tqdm import tqdm
from dotenv import load_dotenv
from openai import OpenAI

# -----------------------------
# PATHS
# -----------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
load_dotenv(os.path.join(BASE_DIR, ".env"))

INPUT_FILE = os.path.join(BASE_DIR, "data", "summary_clues.json")
COMPONENT_FILE = os.path.join(BASE_DIR, "data", "components_final.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "results", "case2", "p1_last_result.json")

MODEL_NAME = "gpt-4o-mini"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------
# HELPERS
# -----------------------------
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_existing(path):
    if os.path.exists(path):
        return load_json(path)
    return []

def extract_json(text):
    if not text:
        return None

    text = text.strip()

    try:
        return json.loads(text)
    except Exception:
        pass

    fenced = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced:
        try:
            return json.loads(fenced.group(1))
        except Exception:
            pass

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start:end + 1]
        try:
            return json.loads(candidate)
        except Exception:
            return None

    return None

def query_llm(prompt):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a careful software engineering assistant. Return valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()

def format_component(comp):
    desc = comp.get("description_object", {})
    owners = comp.get("owners_info", {})

    readme = desc.get("README", {})
    readme_text = readme.get("text", "")

    source_files = desc.get("source_files", [])[:10]
    code_headers = desc.get("code_headers", [])[:5]

    header_lines = []
    for h in code_headers:
        file_name = h.get("file", "")
        header_text = h.get("header", "")
        header_lines.append(f"- {file_name}: {header_text[:300]}")

    component_text = f"""
Component Path: {comp.get("component_path", "")}
SIG Labels: {owners.get("sig_labels", [])}
Area Labels: {owners.get("area_labels", [])}
Other Labels: {owners.get("other_labels", [])}
Description: {readme_text[:1000]}
Source Files: {source_files}
Code Headers:
{chr(10).join(header_lines)}
""".strip()

    return component_text

def build_component_text(components):
    return "\n\n-----------------\n\n".join(format_component(c) for c in components)

def clues_to_text(clues):
    if isinstance(clues, list):
        return "\n".join(f"- {c}" for c in clues)
    if isinstance(clues, str):
        return clues
    return json.dumps(clues, ensure_ascii=False)

def build_prompt(summary, clues, component_text):
    clues_text = clues_to_text(clues)

    return f"""
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
""".strip()

def normalize_prediction(pred_path, valid_paths):
    if pred_path in valid_paths:
        return pred_path
    if pred_path == "NONE":
        return "NONE"
    return "NONE"

# -----------------------------
# MAIN
# -----------------------------
def main():
    summary_clues_data = load_json(INPUT_FILE)
    components = load_json(COMPONENT_FILE)

    valid_paths = [c.get("component_path", "") for c in components if c.get("component_path")]
    component_text = build_component_text(components)

    results = load_existing(OUTPUT_FILE)
    done_ids = {r["thread_id"] for r in results}

    pbar = tqdm(summary_clues_data, desc="Case 2", ncols=100)

    for item in pbar:
        thread_id = item.get("thread_id")

        if thread_id in done_ids:
            continue

        pbar.set_postfix_str(thread_id)

        if item.get("parse_error"):
            results.append({
                "thread_id": thread_id,
                "prompt_id": "p1",
                "component_path": None,
                "confidence": None,
                "rationale": None,
                "error": "SUMMARY_CLUES_PARSE_FAIL"
            })
            save_json(OUTPUT_FILE, results)
            continue

        summary = item.get("summary", "")
        clues = item.get("clues", [])

        prompt = build_prompt(summary, clues, component_text)

        raw_output = query_llm(prompt)
        parsed = extract_json(raw_output)

        if not parsed:
            results.append({
                "thread_id": thread_id,
                "prompt_id": "p1",
                "component_path": None,
                "confidence": None,
                "rationale": None,
                "error": "PARSE_FAIL",
                "raw_output": raw_output
            })
            save_json(OUTPUT_FILE, results)
            continue

        pred_path = normalize_prediction(parsed.get("component_path"), valid_paths)

        results.append({
            "thread_id": thread_id,
            "prompt_id": "p1",
            "component_path": pred_path,
            "confidence": parsed.get("confidence"),
            "rationale": parsed.get("rationale"),
            "error": None
        })

        save_json(OUTPUT_FILE, results)

    print(f"Saved results to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()