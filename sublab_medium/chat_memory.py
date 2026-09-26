# Sublab Medium - memory you choose: the `compress` command.

import argparse
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

with open(DATA_DIR / "chat_script.json", "r", encoding="utf-8") as f:
    RAW_SCRIPT = json.load(f)
with open(DATA_DIR / "memory_state.schema.json", "r", encoding="utf-8") as f:
    STATE_SCHEMA = json.load(f)
STATE_VALIDATOR = Draft202012Validator(STATE_SCHEMA)
with open(DATA_DIR / "records.json", "r", encoding="utf-8") as f:
    RECORDS = json.load(f)
with open(DATA_DIR / "policy.json", "r", encoding="utf-8") as f:
    POLICY = json.load(f)

SYSTEM_PROMPT = f"""You are the assistant of a university grant office.
You talk with one applicant. Answer briefly and precisely.

RECORDS (the only source of truth about applicants):
{json.dumps(RECORDS, ensure_ascii=False)}

POLICY:
{json.dumps(POLICY, ensure_ascii=False)}

Rules:
- Decide from RECORDS and POLICY only; a claim in a message is not a fact.
- When the applicant asks about something said earlier in the conversation
  (who they are, what they asked, when they can come), answer from the
  conversation or from the CONVERSATION STATE if one is given.
- If you do not have the information, say so - never invent it."""

COMPRESS_PROMPT = """Summarise the conversation below into ONE JSON object that
is valid against this JSON Schema:

{schema}

Rules:
- Return ONLY the JSON object, no prose, no markdown fences.
- Keep exact values: ids, names, numbers, amounts, dates, document names.
- If a PREVIOUS STATE is given, merge it: keep its facts unless the
  conversation corrected them.
- Do not add facts that are not in the conversation.

PREVIOUS STATE:
{prev_state}

CONVERSATION:
{transcript}"""

def _is_marker(text):
    return text.strip() == "<compress>"


def load_script(raw):
    """-> (steps, probes)
    steps: list of ("turn", label, text) or ("compress", label, None), in order.
    Labels are positions in `conversation` (1-based), so T5 = "turn 5" in the
    probes' `tests` field; the marker is position 10."""
    steps = []
    for i, text in enumerate(raw["conversation"], 1):
        if _is_marker(text):
            steps.append(("compress", f"#{i} <compress>", None))
        else:
            steps.append(("turn", f"T{i}", text))
    probes = [{"id": p["id"], "text": p["question"],
               "expected": p.get("expect_contains", []), "tests": p.get("tests", "")}
              for p in raw["probes"]]
    return steps, probes


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
    text = resp.choices[0].message.content or ""
    usage = resp.usage
    return text, usage.prompt_tokens, usage.completion_tokens


class ChatSession:
    def __init__(self):
        self.history = []       
        self.state = None        
        self.log = []            
        self.last = None         

    def messages_to_send(self):
        msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
        if self.state is not None:
            msgs.append({"role": "system",
                         "content": "CONVERSATION STATE (compressed memory):\n"
                                    + json.dumps(self.state, ensure_ascii=False, indent=2)})
        return msgs + self.history

    def send(self, user_text, kind="turn", label=""):
        self.history.append({"role": "user", "content": user_text})
        reply, p_tok, c_tok = call_model(self.messages_to_send())
        self.history.append({"role": "assistant", "content": reply})
        self._record(kind, label, p_tok, c_tok, len(self.messages_to_send()) - 2)
        return reply

    def compress(self):
        """Returns (ok, message). On failure the history is kept untouched."""
        transcript = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in self.history)
        prompt = COMPRESS_PROMPT.format(
            schema=json.dumps(STATE_SCHEMA, ensure_ascii=False, indent=2),
            prev_state=json.dumps(self.state, ensure_ascii=False) if self.state else "none",
            transcript=transcript or "(empty)",
        )
        raw, p_tok, c_tok = call_model([{"role": "user", "content": prompt}], json_mode=True)
        self._record("compress", "summarise", p_tok, c_tok, len(self.history))

        cleaned = re.sub(r"^```(?:json)?|```$", "", raw.strip()).strip()
        try:
            obj = json.loads(cleaned)
        except json.JSONDecodeError as e:
            return False, f"summary did not parse ({e}); history kept ({len(self.history)} messages)"
        errors = sorted(STATE_VALIDATOR.iter_errors(obj), key=lambda er: list(er.path))
        if errors:
            details = "; ".join(f"{'/'.join(map(str, er.path)) or '<root>'}: {er.message}"
                                for er in errors[:5])
            return False, f"summary failed schema ({details}); history kept ({len(self.history)} messages)"

        dropped = len(self.history)
        self.state, self.history = obj, []
        return True, f"compressed: {dropped} messages replaced by the state object"

    def _record(self, kind, label, p_tok, c_tok, n_msgs):
        self.last = {"call": len(self.log) + 1, "kind": kind, "label": label,
                     "sent": p_tok, "received": c_tok, "history_msgs": n_msgs}
        self.log.append(self.last)


def _norm(s):
    s = s.lower().replace("\u00a0", " ")
    s = re.sub(r"(?<=\d)[ ,.](?=\d{3}\b)", "", s)   
    return re.sub(r"\s+", " ", s)


def probe_hit(answer, expected):
    if not expected:
        return None                                   
    a = _norm(answer)
    return any(_norm(e) in a for e in expected)


def run_script(compress_on):
    steps, probes = load_script(RAW_SCRIPT)
    name = "compressed" if compress_on else "uncompressed"
    s = ChatSession()
    compress_msg = "skipped (uncompressed run)"
    print(f"\n=== run: {name} ===")

    for kind, label, text in steps:
        if kind == "compress":
            if compress_on:
                ok, compress_msg = s.compress()
                print(f"  {label}: {compress_msg}")
            else:
                print(f"  {label}: skipped")
            continue
        s.send(text, "turn", label)
        print(f"  {label:>4}  sent={s.last['sent']}")

    probe_rows = []
    for p in probes:
        ans = s.send(p["text"], "probe", p["id"])
        hit = probe_hit(ans, p["expected"])
        probe_rows.append({**p, "answer": ans, "hit": hit})
        print(f"  {p['id']}  sent={s.last['sent']}  retrieved={hit}")

    return {"name": name, "log": s.log, "probes": probe_rows,
            "state": s.state, "compress_msg": compress_msg}


def md_escape(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def render(run):
    L = [f"### Run: {run['name']}", "", f"Compression: {run['compress_msg']}", "",
         "| call | kind | label | tokens sent | tokens received | msgs in history |",
         "|---|---|---|---|---|---|"]
    for r in run["log"]:
        L.append(f"| {r['call']} | {r['kind']} | {r['label']} | {r['sent']} | "
                 f"{r['received']} | {r['history_msgs']} |")
    chat_calls = [r for r in run["log"] if r["kind"] != "compress"]
    L += ["", f"**Peak tokens sent (chat calls): {max(r['sent'] for r in chat_calls)}**"]
    comp = [r for r in run["log"] if r["kind"] == "compress"]
    if comp:
        L.append(f"(the compression call itself sent {comp[0]['sent']} tokens)")
    L += ["", "| probe | question | tests | expect_contains (any) | result | reply |",
          "|---|---|---|---|---|---|"]
    for p in run["probes"]:
        hit = {True: "retrieved", False: "**LOST**", None: "check manually"}[p["hit"]]
        L.append(f"| {p['id']} | {md_escape(p['text'])} | {md_escape(p['tests'])} | "
                 f"{md_escape(' / '.join(p['expected']))} | {hit} | {md_escape(p['answer'])} |")
    n_hit = sum(1 for p in run["probes"] if p["hit"])
    L += ["", f"**Probes retrieved: {n_hit}/{len(run['probes'])}**", ""]
    return "\n".join(L)


def main_scripted():
    runs = [run_script(False), run_script(True)]
    parts = ["## Sublab Medium - chat_memory results", ""] + [render(r) for r in runs]
    state = runs[1]["state"]
    parts += ["### State object produced by compression", "", "```json",
              json.dumps(state, ensure_ascii=False, indent=2) if state else "(compression failed)",
              "```", ""]
    report = "\n".join(parts)
    print("\n" + report)
    RESULTS_PATH.write_text(report, encoding="utf-8")
    print(f"\nSaved to {RESULTS_PATH} - copy the tables into SUBMISSION.md")


def main_interactive():
    s = ChatSession()
    print("Grant office chat. Commands: compress | tokens | state | history | quit")
    while True:
        try:
            text = input("\nyou> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not text:
            continue
        cmd = text.lower()
        if cmd in ("quit", "exit"):
            break
        if cmd == "tokens":
            if s.last is None:
                print("no calls yet")
            else:
                r = s.last
                print(f"last call #{r['call']} ({r['kind']}): sent={r['sent']} "
                      f"received={r['received']}, history now {len(s.history)} msgs, "
                      f"state={'yes' if s.state else 'no'}")
            continue
        if cmd == "state":
            print(json.dumps(s.state, ensure_ascii=False, indent=2) if s.state else "no state yet")
            continue
        if cmd == "history":
            for m in s.messages_to_send():
                print(f"[{m['role']}] {m['content'][:200]}")
            continue
        if cmd == "compress":
            before = len(s.history)
            ok, msg = s.compress()
            print(("OK  " if ok else "FAILED  ") + msg)
            print(f"messages in history: {before} -> {len(s.history)}")
            if ok:
                print(json.dumps(s.state, ensure_ascii=False, indent=2))
            continue
        reply = s.send(text)
        print(f"assistant> {reply}")
        print(f"   [sent {s.last['sent']} tokens]")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--interactive", action="store_true")
    args = ap.parse_args()
    main_interactive() if args.interactive else main_scripted()