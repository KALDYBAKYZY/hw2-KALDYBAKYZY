# HW2 submission

**Name:**
**Student ID:**
**Group:**
**Repository:**

## AI tool disclosure

State which AI tools you used and for what. Expected and fine; undisclosed use
is not. If you used a model to help you draft a prompt, say which prompt.

>

---

## Sublab Easy — one task, four roles

### Decisions per role

One row per enquiry. In each cell write the `decision` your run returned, and
whether it agrees with `expected` in `data/enquiries.json`:

| Enquiry | policy_officer | front_desk | auditor | bilingual_clerk |
|---|---|---|---|---|
| E-01 | granted (agrees) | granted (agrees) | more_info (differs) | granted (agrees) |
| E-02 | more_info (agrees) | more_info (agrees) | more_info (agrees) | more_info (agrees) |
| E-03 | refused (agrees) | more_info (differs) | more_info (differs) | refused (agrees) |
| E-04 | refused (agrees) | more_info (differs) | more_info (differs) | refused (agrees) |
| E-05 | granted (agrees) | granted (agrees) | more_info (differs) | granted (agrees) |
| E-06 | granted (agrees) | granted (agrees) | more_info (differs) | granted (agrees) |
| E-07 | granted (agrees) | granted (agrees) | more_info (differs) | granted (agrees) |
| E-08 | not_found (agrees) | not_found (agrees) | not_found (agrees) | not_found (agrees) |
| E-09 | refused (agrees) | more_info (differs) | more_info (differs) | refused (agrees) |
| E-10 | more_info (agrees) | more_info (agrees) | more_info (agrees) | more_info (agrees) |
| **agrees with `expected`** | 10/10 | 7/10 | 3/10 | 10/10 |
| **parsed** | 10/10 | 10/10 | 10/10 | 10/10 |
| **schema-valid** | 10/10 | 10/10 | 10/10 | 10/10 |

### Which field moved, on which enquiry, under which role

| Field | Enquiries that moved | Role(s) that moved it |
|---|---|---|
| `found` | none | no role moved this field |
| `decision` | E-01, E-03, E-04, E-05, E-06, E-07, E-09 | auditor (all 7 of these); front_desk (E-03, E-04, E-09) |
| `amount` | E-01, E-05, E-06, E-07 | auditor |
| `missing_documents` | none | no role moved this field |

Fields that moved on no enquiry: say so explicitly rather than leaving the row
out.

### Raw replies

Paste the full reply for **one enquiry where a role changed the decision** away
from the policy officer's:

```
{
"applicant_id": "A-201",
"found": true,
"decision": "more_info",
"amount": 0,
"missing_documents": [],
"reason": "The file meets the criteria on a first reading: GPA 3.4 meets the minimum threshold of 2.67, income band 1 is allowed, and both required documents are on file. It is queued for a second reader before any money moves."
}
```

Paste the full reply for **E-07 (the Kazakh enquiry)** from the bilingual
clerk, so the `reason` language is visible:

```
{
"applicant_id": "A-201",
"found": true,
"decision": "granted",
"amount": 250000,
"missing_documents": [],
"reason": "GPA 3.4 және табыс санаты 1, транскрипт пен жеке куәлік құжаттары толық бар."
}
```


### Written answers

**1. Which fields are role-sensitive and which are not?** Point at rows in your
tables.

> `found` and `missing_documents` are not role-sensitive: all four roles agree on every enquiry, because these two fields come only from `records.json`, not from the role text. `decision` is the most role-sensitive field: front_desk changes it on E-03, E-04, E-09 (the three "refused" cases), and auditor changes it on 7 of 10 enquiries, almost every one except E-02, E-08 and E-10. `amount` only changes for auditor, and only together with `decision`, because auditor never grants, so amount stays 0 even where policy_officer would pay out. bilingual_clerk changes none of the four structured fields — the only thing it changes is the `reason` text on E-07 (Kazakh instead of English).

**2. Which enquiries are most sensitive to the role, and why those?** Say what
E-03, E-04, E-07 and E-10 are each testing.

> E-03 and E-04 both test what a role does when the applicant fails one condition and no document can fix it (bad GPA for E-03, wrong income band for E-04). These are the enquiries where the roles disagree the most: policy_officer and bilingual_clerk say "refused", front_desk turns it into "more_info" with an explanation, auditor says "more_info" no matter what. E-07 tests language: it is the same applicant as E-01 but written in Kazakh, so it checks if the role still finds the right person and, for bilingual_clerk, if it answers in Kazakh. E-10 tests trust: the applicant claims they already sent a document, but the record still shows it missing. In my run, all four roles ignored the applicant's claim and kept `id_card` as missing, so E-10 did not move anything — that is the correct result, since the rule is to trust only the record.

**3. Where does discretion belong — the role paragraph, or code that reads
`decision` afterwards?** Say what a downstream program can and cannot tell
about which role produced a record.

> A program that only reads `decision` cannot tell why a reply says "more_info". For policy_officer, it means a document is really missing. For auditor, on E-01 it means everything is fine and is only waiting for a second reader. For front_desk on E-03, it means the applicant actually failed a rule, just worded softly. Same word, three different meanings. So the wording and tone can stay in the role paragraph, but any real decision the program has to act on — can money be sent, does a human need to check the case — should be computed by code from `records.json` and `policy.json`, not guessed from which role wrote the JSON.

**4. Is a role a boundary?** Say in Week 2 terms what the role paragraph is
made of, and what you would put in code — not in the prompt — if a wrong
`decision` were expensive.

> No, a role is not a real boundary. A role paragraph is just more text in the system prompt, and the model is only continuing text, not obeying a rule it cannot break. "Auditor never grants" works because the model is following an instruction, not because something outside the model is stopping it. A role paragraph is made of style and priorities: how to talk to the applicant, what to check first, how strict to be. If a wrong `decision` would cost real money, that check cannot live only in the prompt — the code itself must recompute eligibility from `records.json` and `policy.json` and decide if money can actually be sent, using the model's JSON only as a draft for a human, not as the final authority.

---

## Sublab Medium — memory you choose

### Tokens per call

| Call | A — never compressed | B — compressed at the `compress` turn |
|---|---|---|
| 1 (T1) | 752 | 752 |
| 2 (T2) | 801 | 807 |
| 3 (T3) | 883 | 909 |
| 4 (T4) | 940 | 988 |
| 5 (T5) | 988 | 1033 |
| 6 (T6) | 1061 | 1122 |
| 7 (T7) | 1112 | 1190 |
| 8 (T8) | 1187 | 1282 |
| 9 (T9) | 1267 | 1370 |
| 10 (`<compress>`) | — (skipped) | 1110 (the compress call) |
| 11 (T11) | 1324 | 1003 |
| 12 (T12) | 1387 | 1060 |
| **peak** | 1387 (1575 with probes) | 1370 (1370 with probes) |
| **total for the run** | 11702 (19207 with probes) | 12626 (18491 with probes) |

Probe calls (tokens sent): A — 1428, 1464, 1497, 1541, 1575. B — 1099, 1135, 1171, 1214, 1246.

### Probes after the conversation

| Probe | Tests | A retrieved? | A answer | B retrieved? | B answer |
|---|---|---|---|---|---|
| Q-1 identity | turn 1 | yes | You are Daniyar Qoshan, applicant A-202. | yes | You are Daniyar Qoshan, applicant A-202. |
| Q-2 missing document | turn 5 | yes | Your ID card is still missing. | yes | Your ID card is still missing from your file. |
| Q-3 band and amount | turns 3–4 | yes | Your recorded income band is 2, which corresponds to a grant of 150,000 KZT. | yes | Your income band is 2, corresponding to a grant amount of 150,000 KZT. |
| Q-4 the constraint | turn 6 | yes | You said you can come to the office on Thursdays. | yes | You can come to the office on Thursdays. |
| Q-5 the open question | turn 7 | yes | You asked whether a scanned letter from your employer would count, or whether the original was required. | yes | You asked whether a scanned letter from your employer is accepted or whether the original is required. |
| **retrieved** | | 5/5 | | 5/5 | |

### The state my compression produced

```json
{
  "applicant_id": "A-202",
  "topic": "Study grant eligibility, required documents, grant amount, and submission timing",
  "facts": [
    "The applicant's name is Daniyar Qoshan.",
    "The applicant sent their transcript last week.",
    "The applicant's income band is 2, according to their family's certificate.",
    "The applicant could not upload their id_card because their home scanner broke.",
    "The applicant has laboratory classes all week except Thursday.",
    "The applicant stated that their sister Aruzhan applied last year and is also on file."
  ],
  "decisions": [],
  "constraints": [
    "The applicant can come to the office only on Thursdays.",
    "The transcript and id_card are required for the grant application.",
    "The id_card must be uploaded or presented to the university admissions office before the application can qualify."
  ],
  "open_questions": [
    "Whether a scanned letter from the employer is accepted or the original is required.",
    "Whether the grant decision will be made on the same day if the applicant brings the id_card on Thursday."
  ],
  "language": "English and Kazakh"
}
```

### Written answers

**1. What did compression buy?** Peak tokens both ways, probes retrieved both
ways, and — if a probe was lost — which one and which turn it came from.

> The peak without compression was 1575 tokens (the last probe). With compression the peak was 1370 tokens, at T9, before compression. After compression, the calls became smaller: T11 was 1003 tokens, and the last probe was 1246 tokens, not 1575. Both runs retrieved 5 of 5 probes, so no probe was lost. The Thursday fact and the employer question stayed because the schema has `constraints` and `open_questions` fields. But the saving is small in total (18491 vs 19207 tokens), because the conversation is short and the compress call also costs tokens. In a long chat the saving would be much bigger.

**2. Why must the state be structured rather than a paragraph?** You could have
asked for "a summary". Say what changes when the summary is an object with
named fields.

> With named fields, my program can check the summary with the schema. If a field is missing or the JSON is broken, the program does not delete the history. A paragraph cannot be checked like this. Also, the fields make the model think about every category. For example, it must fill `constraints` and `open_questions`. In a normal paragraph, the model would maybe forget small things like "only Thursdays", because they are not about the grant decision. The code can also read the fields directly, for example `applicant_id`.

**3. What is missing from your state that you would add?** Name what you would
add and what you would drop to pay for it.

> My state only has what the applicant said. It does not have what the office answered. `decisions` is empty, but in the chat we found that A-202 can get 150,000 KZT when the ID card is on file. I would add a `status` field (for example "eligible after id_card, 150,000 KZT") and an `answers_given` field, so the assistant remembers what it already told the applicant. To pay for this, I would drop `topic`, because it is a long sentence and nobody uses it later.

**4. When is compression the wrong choice?** Name a conversation where it would
lose something that cannot be recovered, and say whether your program would
notice.

> Compression is bad when the exact words are important. For example, the applicant writes the text of an appeal letter, or first says "my band is 2" and later says "sorry, it is 1". The summary keeps only a short version, and the old messages are deleted, so we cannot get the exact words back. My program would not notice. It only checks that the JSON has the right form, not that the facts are true or complete. In my own state, the model added "admissions office", which nobody said, and the check still passed.

## Sublab Hard — stories in, CVs out, the best candidate by code

File: `sublab_hard/cv_extract_and_rank.py` · output: `sublab_hard/results.md`

### Part 1 — extraction

The rules are in `RULES` and `ADDED_RULES` in the prompt (not null → never estimated, GPA converted to 4.0 with the original scale, only published/accepted papers count, contradictions → null + recorded, evidence quote for every filled field). The rubric's counting rules are also in the prompt.

Rule I added (rule 6): experience months count only from a written start month and end month. A number of months without dates, "today", "continuing" and "about forty months" are not countable.

| Story | Parsed | Valid | Null fields | Traps hit |
|---|---|---|---|---|
| story-01 | yes | yes | none | none |
| story-02 | yes | yes | graduation_year, gpa_4_scale, gpa_original_scale, experience_months | no GPA → null (not estimated); experience "thirty-six months … continuing today" has no dates → null |
| story-03 | yes | yes | none | GPA 4.6 on 5.0 scale → 3.68 on 4.0, scale kept; 1 paper under review, not counted |
| story-04 | yes | yes | none | 3 papers not published (under review, in preparation ×2), not counted |
| story-05 | yes | yes | none | story in Kazakh; 1 paper in preparation, not counted |
| story-06 | yes | yes | degree, graduation_year, gpa_4_scale, gpa_original_scale, experience_months | GPA 3.2 vs 3.5 → contradiction, null; graduated 2024 vs graduating 2026 → contradiction, null; "about forty months", no end date → null; poster not counted |

### Part 2 — scores from the model, total and winner from the code

The model returns only three fields (`academic`, `research`, `experience`, 0–5). The code computes `0.5 * academic + 0.3 * research + 0.2 * experience`, rounded to 2 decimals, sorts the totals and names the winner.

| Rank | Story | Name | Academic | Research | Experience | Total (code) |
|---|---|---|---|---|---|---|
| 1 | story-01 | Aziza Bekova | 5 | 5 | 2 | **4.40** |
| 2 | story-04 | Tamerlan Saparov | 4 | 2.5 | 5 | 3.75 |
| 3 | story-05 | Аиша Нұрланқызы | 5 | 2.5 | 1.25 | 3.50 |
| 4 | story-03 | Lyazzat Omarova | 4 | 2.5 | 3 | 3.35 |
| 5 | story-02 | Dias Yerzhanov | 2.5 | 2.5 | 0 | 2.00 |
| 6 | story-06 | Nurzhan Abilov | 2 | 2.5 | 0 | 1.75 |

**Winner (computed in code): story-01 — Aziza Bekova, total 4.40.** Gap between #1 and #2: 0.65.

#### Prose answer (separate call)

> Aziza Bekova should receive the funded place.
>
> She has the strongest overall evidence under the stated rules: a 3.8 GPA on a 4.0 scale, two published peer-reviewed outputs, and eight months of directly relevant work. Both publications count because the story explicitly says they were published; there is no need to count any merely submitted or planned work.
>
> The closest alternatives are weaker in important respects. Aisha Nurlankyzy has a slightly higher GPA, but only one published paper and six months of experience. Tamerlan Saparov has 24 months of relevant work, but his GPA is 3.6 and only one of his four listed research items is published; the other three must not be counted. Lyazzat Omarova has a strong stated record—4.6/5.0, equivalent to 3.68/4.0—and 14 months of internships, but only one published paper. Dias Yerzhanov and Nurzhan Abilov have substantial work experience, but Dias provides no GPA and Nurzhan's GPA is contradictory, so neither can receive a reliable academic score.
>
> Using a reasonable intermediate scoring scheme—five for the stated top benchmark, half credit for one of two publications, and experience capped at five points at 24 months—Aziza ranks first with an illustrative weighted total of about 4.33/5. Her advantage in both academic record and published research outweighs her shorter work experience.

### Part 3 — written answers

**1. Which rule did you have to add, and what broke without it?**
I added a rule about experience: months count only when the story gives a start month and an end month. Without it, the model counted "thirty-six months" for story-02 (Dias) and "about forty months" for story-06 (Nurzhan), and both got experience 5. Story-02 forced this rule, because it has no dates, only "continuing today". My first version still allowed "an exact number of months", so story-02 still got 36. After I changed it to "dates only", both became null.

**2. Where did the model guess, and where did your code decide?**
The model guessed: story-02 has no GPA, and the rubric says no GPA = 0 on academic, but the model gave 2.5 (in other runs 2 and 0). The code decided the total and the winner: for story-01 it computed 0.5·5 + 0.3·5 + 0.2·2 = 4.40, sorted all totals and chose the highest.

**3. Did the prose ranking and the computed ranking agree?**
They agreed on the winner, Aziza Bekova (story-01). But not below her: the prose says Aisha is the closest, my code puts Tamerlan second. The prose also made its own total, "about 4.33", but my code computed 4.40. I trust the computed ranking, because the scores are fields and the total is computed the same way for everyone. A number inside a sentence cannot be checked or compared.

**4. The rubric has no anchor for a contradicted field. What did you do?**
Story-06 says GPA 3.2 and then 3.5. The field became null and the contradiction was recorded. I gave no special rule to the scoring model, so it decided itself: academic 0, then 1, then 2 in three runs. This is a gap in the rubric. I think a contradicted field should not be scored like "no GPA". The candidate should be marked "check by a person", and the committee should ask the candidate before ranking.

**5. How close were the top two?**
Story-01 had 4.40 and story-04 had 3.75, a gap of 0.65, so it was not close. If the gap was under 0.05, I would tell the committee it is a tie, because the model scores change between runs (Dias academic: 2, 0, 2.5). To make the decision defensible, I would count months from dates in my code, keep an evidence quote for every number, and run the scoring several times to check that the order stays the same.