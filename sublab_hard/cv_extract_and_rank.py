# Sublab Hard - stories in, CVs out, the best candidate by code.

import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, BadRequestError
from jsonschema import Draft202012Validator

load_dotenv()
MODEL = "gpt-5.6-luna"
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
RESULTS_PATH = Path(__file__).resolve().parent / "results.md"

with open(DATA_DIR / "candidate_rubric.json", "r", encoding="utf-8") as f:
    RUBRIC = json.load(f)
WEIGHTS = {c["id"]: c["weight"] for c in RUBRIC["criteria"]}  

CV_SCHEMA = {
    "type": "object",
    "required": ["candidate_id", "full_name", "degree", "graduation_year",
                 "gpa_4_scale", "gpa_original_scale", "languages",
                 "published_count", "unpublished_outputs",
                 "experience_months", "evidence", "contradictions"],
    "properties": {
        "candidate_id": {"type": "string"},
        "full_name": {"type": ["string", "null"]},
        "degree": {"type": ["string", "null"]},
        "graduation_year": {"type": ["integer", "null"]},
        "gpa_4_scale": {"type": ["number", "null"], "minimum": 0, "maximum": 4},
        "gpa_original_scale": {"type": ["number", "null"]},
        "languages": {"type": "array", "items": {"type": "string"}},
        "published_count": {"type": ["integer", "null"], "minimum": 0},
        "unpublished_outputs": {"type": "array", "items": {"type": "string"}},
        "experience_months": {"type": ["integer", "null"], "minimum": 0},
        "evidence": {"type": "object", "additionalProperties": {"type": "string"}},
        "contradictions": {"type": "array", "items": {"type": "string"}},
    },
}
CV_VALIDATOR = Draft202012Validator(CV_SCHEMA)

SCORE_SCHEMA = {
    "type": "object",
    "required": ["academic", "research", "experience"],
    "additionalProperties": False,
    "properties": {c: {"type": "number", "minimum": 0, "maximum": 5} for c in WEIGHTS},
}
SCORE_VALIDATOR = Draft202012Validator(SCORE_SCHEMA)

# ---------------------------------------------------------------- prompts
RULES = """\
1. A fact the story does not state is null. Never estimate it.
   No GPA means gpa_4_scale is null - never an inferred one.
2. A GPA on another scale is converted to a 4.0 scale, and the original scale
   is recorded in gpa_original_scale (4.0 if the story already used 4.0).
3. A paper is published only when the story says published or accepted.
   Submitted, under review, in preparation and in press are NOT published:
   list them in unpublished_outputs and do not count them in published_count.
4. Contradictions are not resolved and not averaged: the field is null,
   and the contradiction is written in contradictions.
5. For every field you fill, put an exact quote from the story in evidence,
   under the same field name."""

# Rule added after the first run (Part 3, question 1). Write it here.
ADDED_RULES = """\
6. Experience months are counted only from a written start month AND end month.
   A number of months without dates ("thirty-six months"), "today", "continuing"
   and "about forty months" are not countable: experience_months is null,
   and the reason goes in contradictions.
"""

EXTRACT_PROMPT = """Extract a CV record from the applicant's story below.
Return ONLY one JSON object, no prose, no markdown fences, valid against this JSON Schema:

{schema}

RULES:
{rules}
{added}
COUNTING RULES FROM THE RUBRIC:
{counting}

CANDIDATE ID: {cid}

STORY:
{story}"""

SCORE_PROMPT = """Score this scholarship candidate against the rubric.

RUBRIC CRITERIA:
{criteria}

COUNTING RULES:
{counting}

CANDIDATE CV RECORD:
{record}

Give a score from 0 to 5 for each of the three criteria. Do not compute a total.
Return ONLY this JSON object: {{"academic": 0-5, "research": 0-5, "experience": 0-5}}"""

PROSE_PROMPT = """You advise a scholarship committee. There is one funded place.

RUBRIC:
{rubric}

STORIES:
{stories}

Which candidate should win, and why? Answer in prose."""


# ---------------------------------------------------------------- helpers
def call_model(messages, json_mode=False):
    kwargs = {"model": MODEL, "messages": messages, "temperature": 0}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    try:
        resp = client.chat.completions.create(**kwargs)
    except BadRequestError as e:
        if "temperature" not in str(e):
            raise
        kwargs.pop("temperature")
        resp = client.chat.completions.create(**kwargs)
    return resp.choices[0].message.content or ""


def parse(text):
    """-> dict or None (no repair, so the table shows what really came back)"""
    text = re.sub(r"^```(json)?|```$", "", text.strip()).strip()
    try:
        obj = json.loads(text)
        return obj if isinstance(obj, dict) else None
    except json.JSONDecodeError:
        return None


def traps_hit(rec):
    traps = []
    if rec.get("gpa_4_scale") is None:
        traps.append("no GPA / GPA not clear -> null")
    elif rec.get("gpa_original_scale") not in (None, 4, 4.0):
        traps.append(f"GPA on {rec['gpa_original_scale']} scale -> converted to {rec['gpa_4_scale']}")
    if rec.get("unpublished_outputs"):
        traps.append(f"{len(rec['unpublished_outputs'])} not published, not counted")
    for c in rec.get("contradictions", []):
        traps.append(f"contradiction: {c}")
    return "; ".join(traps) or "none"


# ---------------------------------------------------------------- main
def main():
    counting = json.dumps(RUBRIC["counting_rules"], ensure_ascii=False, indent=1)
    stories = {p.stem: p.read_text(encoding="utf-8")
               for p in sorted((DATA_DIR / "candidates").glob("story-*.md"))}

    # Part 1 - extract
    records, trap_rows = {}, []
    for cid, story in stories.items():
        print("extract", cid)
        prompt = EXTRACT_PROMPT.format(schema=json.dumps(CV_SCHEMA), rules=RULES,
                                       added=ADDED_RULES, counting=counting,
                                       cid=cid, story=story)
        reply = call_model([{"role": "user", "content": prompt}], json_mode=True)
        rec = parse(reply)
        if rec is None:
            trap_rows.append(f"| {cid} | no | - | - | - |")
            continue
        errors = list(CV_VALIDATOR.iter_errors(rec))
        nulls = [k for k in CV_SCHEMA["required"] if rec.get(k) is None]
        trap_rows.append(f"| {cid} | yes | {'yes' if not errors else 'no'} | "
                         f"{', '.join(nulls) or 'none'} | {traps_hit(rec)} |")
        records[cid] = rec

    # Part 2 - the model scores, the code ranks
    rows = []
    for cid, rec in records.items():
        print("score", cid)
        prompt = SCORE_PROMPT.format(criteria=json.dumps(RUBRIC["criteria"], indent=1),
                                     counting=counting,
                                     record=json.dumps(rec, ensure_ascii=False, indent=1))
        scores = parse(call_model([{"role": "user", "content": prompt}], json_mode=True))
        if scores is None or list(SCORE_VALIDATOR.iter_errors(scores)):
            print("  score reply not valid, skipped:", scores)
            continue
        total = round(sum(WEIGHTS[c] * scores[c] for c in WEIGHTS), 2)
        rows.append((total, cid, rec.get("full_name"), scores))
    rows.sort(key=lambda r: -r[0])

    print("prose ranking")
    prose = call_model([{"role": "user", "content": PROSE_PROMPT.format(
        rubric=json.dumps(RUBRIC, ensure_ascii=False, indent=1),
        stories="\n\n".join(f"=== {cid} ===\n{s}" for cid, s in stories.items()))}])

    # report
    out = ["# Sublab Hard - results", "",
           "## Part 1 - extraction", "",
           "| Story | Parsed | Valid | Null fields | Traps hit |", "|---|---|---|---|---|",
           *trap_rows, "",
           "## Part 2 - scores (model) and total (code)", "",
           "| Rank | Story | Name | Academic | Research | Experience | Total |",
           "|---|---|---|---|---|---|---|"]
    for i, (total, cid, name, s) in enumerate(rows, 1):
        out.append(f"| {i} | {cid} | {name} | {s['academic']} | {s['research']} | "
                   f"{s['experience']} | {total:.2f} |")
    if rows:
        out += ["", f"**Winner (computed in code): {rows[0][1]} - {rows[0][2]}, total {rows[0][0]:.2f}**"]
    if len(rows) > 1:
        out.append(f"Gap between #1 and #2: {rows[0][0] - rows[1][0]:.2f}")
    out += ["", "## Part 2 - prose answer (separate call)", "", prose, "",
            "## Records", "", "```json",
            json.dumps(records, ensure_ascii=False, indent=2), "```"]
    RESULTS_PATH.write_text("\n".join(out), encoding="utf-8")
    print("written", RESULTS_PATH)


if __name__ == "__main__":
    main()