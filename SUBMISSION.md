# HW2 submission

**Name: Zhaiylgan Gulnaz**
**Student ID: s23067637**
**Group: CSS4007-ENG-10**
**Repository: hw2-KALDYBAKYZY**

## AI tool disclosure

State which AI tools you used and for what. Expected and fine; undisclosed use
is not. If you used a model to help you draft a prompt, say which prompt.

>I used Claude (Anthropic). Claude wrote the code for all three sublabs. Then it helped me to understand the code, function by function, so I can explain it. At the end, it checked my SUBMISSION.md: it showed me the weak points and what I forgot, and it helped me to write my answers in simple English. I ran all three programs myself, and all numbers and replies in this file are from my own runs.

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
 
The full table for each role (parsed, schema-valid, and match or MOVED for
`found`, `decision`, `amount`, `missing_documents`) and all 40 replies are in
`sublab_easy/results.md`.
 
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
 
> `found` and `missing_documents` do not change: all roles give the same value on every enquiry, because they come from `records.json`. `decision` changes the most: front_desk moves it on E-03, E-04, E-09, and auditor on 7 of 10 (all except E-02, E-08, E-10). `amount` moves only with auditor, because it never grants, so the amount is 0. So auditor moves `decision`, and bilingual_clerk moves only `reason` (Kazakh on E-07).
 
**2. Which enquiries are most sensitive to the role, and why those?** Say what
E-03, E-04, E-07 and E-10 are each testing.
 
> E-03 (GPA too low) and E-04 (wrong income band) fail a rule that no document can fix. Here the roles differ most: policy_officer and bilingual_clerk say "refused", front_desk and auditor say "more_info". E-07 is E-01 in Kazakh: can the role find the person, and does bilingual_clerk answer in Kazakh? E-10 tests trust: the applicant says "I sent my id card", but the record says no. All roles kept `id_card` missing, which is correct.
 
**3. Where does discretion belong — the role paragraph, or code that reads
`decision` afterwards?** Say what a downstream program can and cannot tell
about which role produced a record.
 
> A program that reads only `decision` cannot know what "more_info" means. From policy_officer it means a missing document, from auditor (E-01) "OK, but check again", from front_desk (E-03) a failed rule said softly. The program cannot see which role wrote it. So the role is for tone, but the real decision (send money or not) must be made by code from `records.json` and `policy.json`.
 
**4. Is a role a boundary?** Say in Week 2 terms what the role paragraph is
made of, and what you would put in code — not in the prompt — if a wrong
`decision` were expensive.
 
> No. In Week 2 terms, the role paragraph is only tokens in the same context, and the model just continues the text. Nothing outside the model stops it from breaking the role. If a wrong `decision` is expensive, my code must check GPA, income band and documents again from the data, and only the code decides if money is sent.
 
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
 
> Peak: 1575 tokens without compression, 1370 with compression (T9, just before compressing). After compression the calls were smaller (last probe 1246, not 1575). Both runs got 5/5 probes, nothing was lost. The total saving is small (18491 vs 19207), because the chat is short and the compress call also costs tokens.
 
**2. Why must the state be structured rather than a paragraph?** You could have
asked for "a summary". Say what changes when the summary is an object with
named fields.
 
> With fields, my code can check the summary with the schema, and if it is broken, the history is not deleted. A paragraph cannot be checked. Fields also make the model fill every part, like `constraints` and `open_questions`, so small things like "only Thursdays" are not forgotten.
 
**3. What is missing from your state that you would add?** Name what you would
add and what you would drop to pay for it.
 
> My state has only what the applicant said, not what the office answered (`decisions` is empty). I would add `status` (for example "eligible after id_card, 150,000 KZT") and `answers_given`. To pay for it, I would drop `topic`, because nobody uses it.
 
**4. When is compression the wrong choice?** Name a conversation where it would
lose something that cannot be recovered, and say whether your program would
notice.
 
> When exact words matter: for example an appeal letter, or "my band is 2" and later "sorry, it is 1". The old messages are deleted, so the exact words are lost. My program would not notice: it checks only the JSON form, not the facts. My state even has "admissions office", which nobody said, and it still passed.
 
## Sublab Hard — stories in, CVs out, the best candidate by code
 
File: `sublab_hard/cv_extract_and_rank.py` · output: `sublab_hard/results.md`
 
### Part 1 — extraction
 
All rules are in the prompt (`RULES`, `ADDED_RULES` and the rubric counting rules): no fact → null; GPA changed to 4.0, old scale saved; only published or accepted papers count; contradiction → null and written down; a quote for every field.
 
Rule I added (rule 6): count experience months only from a start month and an end month.
 
| Story | Parsed | Valid | Null fields | Traps hit |
|---|---|---|---|---|
| story-01 | yes | yes | none | none |
| story-02 | yes | yes | graduation_year, gpa_4_scale, gpa_original_scale, experience_months | no GPA → null (not estimated); experience "thirty-six months … continuing today" has no dates → null |
| story-03 | yes | yes | none | GPA 4.6 on 5.0 scale → 3.68 on 4.0, scale kept; 1 paper under review, not counted |
| story-04 | yes | yes | none | 3 papers not published (under review, in preparation ×2), not counted |
| story-05 | yes | yes | none | story in Kazakh; 1 paper in preparation, not counted |
| story-06 | yes | yes | degree, graduation_year, gpa_4_scale, gpa_original_scale, experience_months | GPA 3.2 vs 3.5 → contradiction, null; graduated 2024 vs graduating 2026 → contradiction, null; "about forty months", no end date → null; poster not counted |
 
The extraction for **story-06**, the story that says two different things (copied from `sublab_hard/results.md`):
 
```json
{
  "candidate_id": "story-06",
  "full_name": "Nurzhan Abilov",
  "degree": null,
  "graduation_year": null,
  "gpa_4_scale": null,
  "gpa_original_scale": null,
  "languages": ["Kazakh", "Russian", "English"],
  "published_count": 1,
  "unpublished_outputs": ["One poster at a local event"],
  "experience_months": null,
  "evidence": {
    "candidate_id": "CANDIDATE ID: story-06",
    "full_name": "# Nurzhan Abilov",
    "degree": "I graduated in 2024 with a BSc in Statistics.",
    "graduation_year": "I graduated in 2024 with a BSc in Statistics. I am currently a final-year student graduating in 2026",
    "gpa_4_scale": "My GPA was 3.2. Actually I should double-check that, I think it was 3.5",
    "gpa_original_scale": "My GPA was 3.2. Actually I should double-check that, I think it was 3.5",
    "languages": "Languages: Kazakh, Russian, English.",
    "published_count": "one paper published, in a peer-reviewed proceedings, on survey weighting.",
    "unpublished_outputs": "One poster at a local event, which I do not think counts.",
    "experience_months": "I have been at an insurance analytics team since February 2023, which is about forty months.",
    "contradictions": "Either way it is somewhere in the low threes."
  },
  "contradictions": [
    "The story says both \"I graduated in 2024 with a BSc in Statistics\" and \"I am currently a final-year student graduating in 2026,\" so degree and graduation year are contradictory.",
    "The GPA is stated as both 3.2 and 3.5, so it cannot be resolved; no grading scale is stated.",
    "Experience has a written start month (February 2023) but no written end month; \"about forty months\" and the ongoing wording are not countable under the rules."
  ]
}
```
 
### Part 2 — scores from the model, total and winner from the code
 
The model gives only three scores (0–5). My code calculates `0.5*academic + 0.3*research + 0.2*experience`, rounds to 2 decimals and chooses the winner.
 
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
 
> Rule 6: count months only from a start month and an end month. Without it, the model counted "thirty-six months" (story-02) and "about forty months" (story-06), and both got 5 for experience. Story-02 forced this rule: it has no dates, only "continuing today". After the rule, both became null.
 
**2. Where did the model guess, and where did your code decide?**
 
> The model guessed: story-02 has no GPA, the rubric says 0, but the model gave 2.5 (in other runs 2 and 0). The code decided: for story-01 it calculated 0.5·5 + 0.3·5 + 0.2·2 = 4.40, then sorted the totals and chose the winner.
 
**3. Did the prose ranking and the computed ranking agree?**
 
> Same winner, Aziza (story-01), but a different second place (prose: Aisha, code: Tamerlan). The prose also made its own total, "about 4.33", but the code got 4.40. I trust the code: the scores are fields and the total is calculated the same way for everyone.
 
**4. The rubric has no anchor for a contradicted field. What did you do?**
 
> The GPA became null and the contradiction was written down. The scoring model had no rule for this and gave academic 0, 1 and 2 in three runs. I think a contradiction is not the same as "no GPA": the candidate should be marked "a person must check" and asked before the ranking.
 
**5. How close were the top two?**
 
> 4.40 vs 3.75, a gap of 0.65, so not close. Under 0.05 I would call it a tie, because the scores change between runs. To make it fair, I would count months from dates in code, keep a quote for every number, and run the scoring a few times.