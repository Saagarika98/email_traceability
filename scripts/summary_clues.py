import json
import os
import re
from tqdm import tqdm
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL_NAME = "gpt-4o-mini"

INPUT_FILE = "data/td_email_threads.json"
OUTPUT_FILE = "data/summary_clues.json"

TARGET_THREAD_IDS = {
    "a-0wx-MeWVo", "bP2_ijXddMs", "jtvEpud5sDc", "xhQuwdd2Smw", "0uBKzd5yrF0",
    "I-kGxTUVzVs", "kd97N7k4Eeo", "5cYBMrHdfjE", "u_rsLcOrvOs", "vtXxsprhyog",
    "Th50olAPPhU", "YI-lOna93RY", "gUBV1b-EnHg", "tJ5Y_av0Bao", "y-eWzF-bmX8",
    "d29C-A5XLc0", "rO-cUwJMixQ", "xnEG7_5WZJI", "FEH9suc_UGo", "cILhJ_mQe9I",
    "YZYSRIpnXmw", "OOaKkcOKJVs", "lfC3v83VwYs", "a2oZ9md7Z8g", "jmxp5ceglnY",
    "IjIKrFh3QVA", "K-9KA_wMbmk", "7nfG0fKcKEU"
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def extract_json(text):
    """
    Parses clean JSON first.
    If the model adds extra text, extracts the first JSON object.
    """
    if not text:
        return None

    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None

    json_text = match.group(0)

    # remove trailing commas if present
    json_text = re.sub(r",\s*}", "}", json_text)
    json_text = re.sub(r",\s*]", "]", json_text)

    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        return None


def query_llm(prompt):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()



def build_summary_clues_prompt(email_thread):
    return f"""
You are extracting structured information from a developer email thread
for component mapping.

EMAIL THREAD
------------
{email_thread}

TASK
----
Extract:

1. A concise technical summary of the discussion, including any relevant
technical debt concerns (such as workarounds, design limitations,
maintenance issues, architectural concerns, testing gaps, or configuration problems).

2. A list of clues that may help identify the responsible system component.

Return JSON only in exactly this format:

{{
  "summary": "",
  "clues": []
}}

FIELD DEFINITIONS
-----------------
summary:
Short technical summary of the discussion including important technical-debt-related information when present.

clues:
Keywords or short phrases useful for component mapping, such as subsystem names,
feature names, APIs, packages, files, configs, errors, or implementation hints.

RULES
-----
- Preserve only information relevant for component mapping.
- Do not invent component paths.
- Do not select the final component.
- Use empty clue list [] if no strong clues exist.
- Return valid JSON only.
"""



def main():
    emails = load_json(INPUT_FILE)

    target_emails = [
        e for e in emails
        if e.get("thread_id") in TARGET_THREAD_IDS
    ]

    found_ids = {e.get("thread_id") for e in target_emails}
    missing_ids = TARGET_THREAD_IDS - found_ids

    if missing_ids:
        print("\nMissing thread IDs from input file:")
        for tid in sorted(missing_ids):
            print(f"- {tid}")

    results = []

    for email in tqdm(target_emails, desc="Extracting summary + clues"):
        thread_id = email.get("thread_id")
        email_thread = email.get("full_thread_text", "")

        if not email_thread.strip():
            results.append({
                "thread_id": thread_id,
                "summary": "",
                "clues": [],
                "error": "Empty full_thread_text"
            })
            save_json(OUTPUT_FILE, results)
            continue

        raw_output = query_llm(
            build_summary_clues_prompt(email_thread)
        )

        parsed = extract_json(raw_output)

        if parsed:
            results.append({
                "thread_id": thread_id,
                "summary": parsed.get("summary", ""),
                "clues": parsed.get("clues", [])
            })
        else:
            results.append({
                "thread_id": thread_id,
                "summary": "",
                "clues": [],
                "parse_error": True,
                "raw_output": raw_output
            })

        save_json(OUTPUT_FILE, results)

    print(f"\nSaved results to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()