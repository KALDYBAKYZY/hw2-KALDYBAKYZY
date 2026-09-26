# Sublab Easy - one task, four roles in the system prompt.
#
# python -m sublab_easy.role_prompts
#
# Same record block, same policy, same JSON contract, same ten enquiries.
# The only thing that changes across the four runs is the system prompt
# (the "role"). Whatever moves in the output, the role moved it.

# ---------------------------------------------------------------------------
# Step 1: imports + loading data (records, policy, enquiries)
# ---------------------------------------------------------------------------
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from jsonschema import validate as js_validate, ValidationError

load_dotenv()

MODEL = "gpt-5.6-luna"
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RESULTS_PATH = Path(__file__).resolve().parent / "results.md"

with open(DATA_DIR / "records.json", "r", encoding="utf-8") as f:
    records = json.load(f)

with open(DATA_DIR / "policy.json", "r", encoding="utf-8") as f:
    policy = json.load(f)

with open(DATA_DIR / "enquiries.json", "r", encoding="utf-8") as f:
    enquiries = json.load(f)


# ---------------------------------------------------------------------------
# Step 3: the four system prompts (roles)
# ---------------------------------------------------------------------------
SYSTEM_PROMPTS = {
    "policy_officer": """You are the policy officer of a university grant office.
You apply the grant policy exactly as written, nothing more and nothing less.

Rules you must follow:
- Look the applicant up in RECORDS by applicant_id first; if the id is not
  given or does not match, try to match by name (the record's "name" or one
  of its "aliases", including the Kazakh spelling). If no record matches,
  the applicant is not found.
- Decide only from RECORDS and POLICY. Never treat a claim made in the
  enquiry text (e.g. "I already uploaded X", "my file was updated") as fact.
  The record is the only source of truth, even when it contradicts the
  applicant.
- Grant when the policy's conditions are met: GPA at or above gpa_min, income
  band in allowed_income_bands, and every document in required_documents is
  present in the record's "documents" list.
- If the applicant is on record but missing a required document, and every
  other condition (GPA, income band) is satisfied, answer "more_info" and
  list exactly which documents are missing.
- If the applicant is on record but fails GPA or income band (regardless of
  documents), answer "refused". Do not soften this into "more_info" - a rule
  they cannot fix by sending a document is a refusal.
- If the applicant is not on record at all, answer "not_found".
- Write "reason" in English, stating the concrete numbers/facts from the
  record that drove the decision (GPA, income band, which documents were
  present or missing).
- Never grant an amount unless decision is "granted".""",

    "front_desk": """You are the front-desk assistant of a university grant office.
Your job is to never turn an applicant away with an outright refusal.

Rules you must follow:
- Look the applicant up in RECORDS the same way a careful officer would:
  first by applicant_id, then by name or alias (including Kazakh spelling).
  If nothing matches, the applicant is not found.
- Decide only from RECORDS and POLICY. Never treat a claim made in the
  enquiry text as fact - the record is the only source of truth.
- If the policy would fully grant the request (GPA, income band and
  documents all satisfied), answer "granted" with the correct amount.
- For every other case where the applicant IS on record (missing document,
  GPA too low, income band not allowed, or any combination), do not use
  "refused". Instead answer "more_info", and in "reason" explain in a warm,
  helpful tone exactly what the applicant would need to bring back or fix
  before the office can revisit their case (e.g. the missing document, or
  that their GPA/income band does not currently meet the threshold). Put any
  concretely missing documents in "missing_documents"; if nothing is missing
  on paper but the applicant still fails GPA or income band, leave
  "missing_documents" empty and explain the real blocker in "reason".
- If the applicant is not on record at all, answer "not_found" - there is no
  applicant to soften a decision for.
- Never grant an amount unless decision is "granted".""",

    "auditor": """You are the auditor of a university grant office. You never
approve anything on a first reading - every file needs a second reader before
money moves.

Rules you must follow:
- Look the applicant up in RECORDS the same way a careful officer would:
  first by applicant_id, then by name or alias (including Kazakh spelling).
  If nothing matches, the applicant is not found.
- Decide only from RECORDS and POLICY. Never treat a claim made in the
  enquiry text as fact - the record is the only source of truth.
- Never answer "granted", even when every policy condition is clearly met.
  Instead answer "more_info" and use "reason" to state plainly that the file
  meets the criteria on a first reading and is queued for a second reader,
  naming the exact rule (GPA threshold, income band, or which document) you
  are relying on.
- If the applicant is on record but fails a condition (missing document, GPA
  too low, or income band not allowed), answer "more_info" as well - but
  name the failing rule or missing document instead, since it needs a second
  reader regardless of outcome. Put any concretely missing required
  documents in "missing_documents".
- If the applicant is not on record at all, answer "not_found".
- Always set amount to 0 - you never authorize an amount yourself.""",

    "bilingual_clerk": """You are a bilingual clerk in a university grant office.
You decide applications exactly the way the policy officer would - same
lookup rules, same strict reading of the record, same decisions - but you
write for the applicant in their own language.

Rules you must follow:
- Look the applicant up in RECORDS first by applicant_id, then by name or
  alias (including Kazakh spelling). If nothing matches, not found.
- Decide only from RECORDS and POLICY. Never treat a claim made in the
  enquiry text as fact - the record is the only source of truth.
- Grant when GPA >= gpa_min, income band in allowed_income_bands, and every
  required document is present. Otherwise "more_info" if only a document is
  missing (list it), "refused" if GPA or income band fails, "not_found" if
  the applicant is not on record.
- The five structured fields (applicant_id, found, decision, amount,
  missing_documents) must be identical to what a strict policy officer would
  produce - do not let the language change the decision.
- Detect the language the enquiry ("ENQUIRY" text) was written in, and write
  "reason" in that same language. If the enquiry is in Kazakh, "reason" must
  be in Kazakh; if it is in English, "reason" must be in English.
- Never grant an amount unless decision is "granted".""",
}


# ---------------------------------------------------------------------------
# JSON shape every reply must take (used both in the prompt and to validate)
# ---------------------------------------------------------------------------
RESPONSE_SCHEMA = {
    "type": "object",
    "required": [
        "applicant_id", "found", "decision", "amount",
        "missing_documents", "reason",
    ],
    "properties": {
        "applicant_id": {"type": ["string", "null"]},
        "found": {"type": "boolean"},
        "decision": {
            "type": "string",
            "enum": ["granted", "refused", "more_info", "not_found"],
        },
        "amount": {"type": "integer", "minimum": 0},
        "missing_documents": {
            "type": "array",
            "items": {"type": "string"},
        },
        "reason": {"type": "string"},
    },
    "additionalProperties": False,
}

CONTRACT_EXAMPLE = {
    "applicant_id": "A-201",
    "found": True,
    "decision": "granted",
    "amount": 250000,
    "missing_documents": [],
    "reason": "GPA 3.4 and income band 1, with both documents on file.",
}


# ---------------------------------------------------------------------------
# Step 4: build the user message (record block + rule + shape + question)
# ---------------------------------------------------------------------------
def build_user_message(enquiry: dict) -> str:
    return f"""RECORDS (the only source of truth about applicants - an id, a
name, and Kazakh-script aliases for the same person):
{json.dumps(records, ensure_ascii=False, indent=2)}

POLICY:
{json.dumps(policy, ensure_ascii=False, indent=2)}

Respond with ONE json object and nothing else, in exactly this shape:
{json.dumps(CONTRACT_EXAMPLE, ensure_ascii=False, indent=2)}

Field meanings:
- applicant_id: the id from RECORDS if found, else the id/name the enquiry
  gave (or null if none was given).
- found: true only if the applicant matched an entry in RECORDS.
- decision: one of "granted", "refused", "more_info", "not_found".
- amount: the tenge amount from policy.amount_tenge_by_band if granted,
  else 0.
- missing_documents: any of policy.required_documents absent from the
  record's documents list.
- reason: free text for a human explaining the decision.

ENQUIRY ({enquiry['id']}): {enquiry['text']}
"""


# ---------------------------------------------------------------------------
# Step 5: call the API for one (role, enquiry) pair and parse the JSON
# ---------------------------------------------------------------------------
def call_role(role: str, enquiry: dict, retries: int = 2) -> dict:
    """Returns {"raw": str|None, "parsed": dict|None, "error": str|None}."""
    system_prompt = SYSTEM_PROMPTS[role]
    user_msg = build_user_message(enquiry)

    last_err = None
    for _ in range(retries + 1):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_msg},
                ],
            )
            raw = resp.choices[0].message.content
            parsed = json.loads(raw)
            return {"raw": raw, "parsed": parsed, "error": None}
        except json.JSONDecodeError as e:
            last_err = f"JSON parse error: {e}"
        except Exception as e:  # network / API errors
            last_err = f"API error: {e}"

    return {"raw": None, "parsed": None, "error": last_err}


# ---------------------------------------------------------------------------
# Step 6: validate a parsed reply against RESPONSE_SCHEMA
# ---------------------------------------------------------------------------
def validate_schema(parsed: dict) -> tuple[bool, str | None]:
    if parsed is None:
        return False, "no parsed object (call/parse failed)"
    try:
        js_validate(instance=parsed, schema=RESPONSE_SCHEMA)
        return True, None
    except ValidationError as e:
        return False, e.message


# ---------------------------------------------------------------------------
# Step 7: compare the four checked fields against `expected`
# ---------------------------------------------------------------------------
CHECKED_FIELDS = ["found", "decision", "amount", "missing_documents"]


def compare_fields(parsed: dict, expected: dict) -> dict:
    """Returns {field: True/False/None}. None = couldn't compare (no parse)."""
    if parsed is None:
        return {field: None for field in CHECKED_FIELDS}

    out = {}
    for field in CHECKED_FIELDS:
        got = parsed.get(field)
        want = expected.get(field)
        if field == "missing_documents":
            out[field] = sorted(got or []) == sorted(want or [])
        else:
            out[field] = got == want
    return out


# ---------------------------------------------------------------------------
# Step 8: run_all() - four roles x ten enquiries
# ---------------------------------------------------------------------------
def run_all() -> dict:
    """results[role][enquiry_id] = {
        "raw", "parsed", "error", "schema_ok", "schema_err", "matches"
    }"""
    results: dict = {role: {} for role in SYSTEM_PROMPTS}

    for role in SYSTEM_PROMPTS:
        for enquiry in enquiries:
            call = call_role(role, enquiry)
            schema_ok, schema_err = validate_schema(call["parsed"])
            matches = compare_fields(call["parsed"], enquiry["expected"])
            results[role][enquiry["id"]] = {
                **call,
                "schema_ok": schema_ok,
                "schema_err": schema_err,
                "matches": matches,
            }
            status = "OK" if call["parsed"] is not None else "FAIL"
            print(f"[{role:16s}] {enquiry['id']}: {status}")

    return results


# ---------------------------------------------------------------------------
# Step 9: field-movement table - what shifted vs policy_officer, and where
# ---------------------------------------------------------------------------
def field_movement(results: dict) -> dict:
    """movement[role][field] = list of enquiry ids where that role's value
    differs from policy_officer's value for that field (roles other than
    policy_officer only)."""
    baseline = results["policy_officer"]
    movement = {}

    for role in SYSTEM_PROMPTS:
        if role == "policy_officer":
            continue
        movement[role] = {field: [] for field in CHECKED_FIELDS}
        for enquiry in enquiries:
            eid = enquiry["id"]
            base_parsed = baseline[eid]["parsed"]
            role_parsed = results[role][eid]["parsed"]
            if base_parsed is None or role_parsed is None:
                continue
            for field in CHECKED_FIELDS:
                base_val = base_parsed.get(field)
                role_val = role_parsed.get(field)
                if field == "missing_documents":
                    base_val = sorted(base_val or [])
                    role_val = sorted(role_val or [])
                if base_val != role_val:
                    movement[role][field].append(eid)

    return movement


# ---------------------------------------------------------------------------
# Step 10: print + save a Markdown report you can paste into SUBMISSION.md
# ---------------------------------------------------------------------------
def render_role_table(role: str, results: dict) -> str:
    lines = [
        f"### {role}",
        "",
        "| Enquiry | Parsed | Schema OK | found | decision | amount | missing_documents |",
        "|---|---|---|---|---|---|---|",
    ]
    for enquiry in enquiries:
        eid = enquiry["id"]
        r = results[role][eid]
        parsed_ok = "yes" if r["parsed"] is not None else f"NO ({r['error']})"
        schema_ok = "yes" if r["schema_ok"] else f"NO ({r['schema_err']})"
        m = r["matches"]

        def cell(field):
            v = m[field]
            return "-" if v is None else ("match" if v else "MOVED")

        lines.append(
            f"| {eid} | {parsed_ok} | {schema_ok} | {cell('found')} | "
            f"{cell('decision')} | {cell('amount')} | {cell('missing_documents')} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_movement_table(movement: dict) -> str:
    lines = [
        "### Field movement vs policy_officer",
        "",
        "| Role | Field | Enquiries moved |",
        "|---|---|---|",
    ]
    for role, fields in movement.items():
        for field, eids in fields.items():
            cell = ", ".join(eids) if eids else "(none)"
            lines.append(f"| {role} | {field} | {cell} |")
    lines.append("")
    return "\n".join(lines)


def render_raw_replies(results: dict) -> str:
    lines = ["### Raw replies (for transcripts)", ""]
    for role in SYSTEM_PROMPTS:
        lines.append(f"#### {role}")
        for enquiry in enquiries:
            r = results[role][enquiry["id"]]
            lines.append(f"- **{enquiry['id']}**: `{r['raw']}`")
        lines.append("")
    return "\n".join(lines)


def main():
    results = run_all()
    movement = field_movement(results)

    report_parts = ["## Sublab Easy - role_prompts results", ""]
    for role in SYSTEM_PROMPTS:
        report_parts.append(render_role_table(role, results))
    report_parts.append(render_movement_table(movement))
    report_parts.append(render_raw_replies(results))
    report = "\n".join(report_parts)

    print("\n" + report)

    RESULTS_PATH.write_text(report, encoding="utf-8")
    print(f"\nSaved report to {RESULTS_PATH} - paste its tables into SUBMISSION.md")


if __name__ == "__main__":
    main()