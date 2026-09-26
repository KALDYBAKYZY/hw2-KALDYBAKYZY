## Sublab Medium - chat_memory results

### Run: uncompressed

Compression: skipped (uncompressed run)

| call | kind | label | tokens sent | tokens received | msgs in history |
|---|---|---|---|---|---|
| 1 | turn | T1 | 752 | 27 | 1 |
| 2 | turn | T2 | 801 | 117 | 3 |
| 3 | turn | T3 | 883 | 98 | 5 |
| 4 | turn | T4 | 940 | 27 | 7 |
| 5 | turn | T5 | 988 | 49 | 9 |
| 6 | turn | T6 | 1061 | 62 | 11 |
| 7 | turn | T7 | 1112 | 116 | 13 |
| 8 | turn | T8 | 1187 | 54 | 15 |
| 9 | turn | T9 | 1267 | 100 | 17 |
| 10 | turn | T11 | 1324 | 49 | 19 |
| 11 | turn | T12 | 1387 | 23 | 21 |
| 12 | probe | Q-1 | 1428 | 20 | 23 |
| 13 | probe | Q-2 | 1464 | 12 | 25 |
| 14 | probe | Q-3 | 1497 | 25 | 27 |
| 15 | probe | Q-4 | 1541 | 18 | 29 |
| 16 | probe | Q-5 | 1575 | 27 | 31 |

**Peak tokens sent (chat calls): 1575**

| probe | question | tests | expect_contains (any) | result | reply |
|---|---|---|---|---|---|
| Q-1 | Which applicant am I, and what is my number? | identity, stated once in turn 1 | A-202 | retrieved | You are **Daniyar Qoshan**, applicant **A-202**. |
| Q-2 | Which document is still missing from my file? | the missing document, turn 5 | id_card / id card | retrieved | Your **ID card** is still missing. |
| Q-3 | What is my income band, and what amount does that come to? | the band from turn 3 and the amount from turn 4 | 150000 / 150,000 | retrieved | Your recorded income band is **2**, which corresponds to a grant of **150,000 KZT**. |
| Q-4 | Which day of the week can I come to the office? | a constraint the applicant stated in turn 6 and never repeated | Thursday | retrieved | You said you can come to the office on **Thursdays**. |
| Q-5 | What did I ask you about my employer? | an open question, turn 7, never answered | letter / employer | retrieved | You asked whether a **scanned letter from your employer** would count, or whether the **original** was required. |

**Probes retrieved: 5/5**

### Run: compressed

Compression: compressed: 18 messages replaced by the state object

| call | kind | label | tokens sent | tokens received | msgs in history |
|---|---|---|---|---|---|
| 1 | turn | T1 | 752 | 33 | 1 |
| 2 | turn | T2 | 807 | 147 | 3 |
| 3 | turn | T3 | 909 | 101 | 5 |
| 4 | turn | T4 | 988 | 24 | 7 |
| 5 | turn | T5 | 1033 | 65 | 9 |
| 6 | turn | T6 | 1122 | 41 | 11 |
| 7 | turn | T7 | 1190 | 111 | 13 |
| 8 | turn | T8 | 1282 | 90 | 15 |
| 9 | turn | T9 | 1370 | 117 | 17 |
| 10 | compress | summarise | 1110 | 613 | 18 |
| 11 | turn | T11 | 1003 | 102 | 2 |
| 12 | turn | T12 | 1060 | 21 | 4 |
| 13 | probe | Q-1 | 1099 | 20 | 6 |
| 14 | probe | Q-2 | 1135 | 15 | 8 |
| 15 | probe | Q-3 | 1171 | 24 | 10 |
| 16 | probe | Q-4 | 1214 | 16 | 12 |
| 17 | probe | Q-5 | 1246 | 58 | 14 |

**Peak tokens sent (chat calls): 1370**
(the compression call itself sent 1110 tokens)

| probe | question | tests | expect_contains (any) | result | reply |
|---|---|---|---|---|---|
| Q-1 | Which applicant am I, and what is my number? | identity, stated once in turn 1 | A-202 | retrieved | You are **Daniyar Qoshan**, applicant **A-202**. |
| Q-2 | Which document is still missing from my file? | the missing document, turn 5 | id_card / id card | retrieved | Your **ID card** is still missing from your file. |
| Q-3 | What is my income band, and what amount does that come to? | the band from turn 3 and the amount from turn 4 | 150000 / 150,000 | retrieved | Your income band is **2**, corresponding to a grant amount of **150,000 KZT**. |
| Q-4 | Which day of the week can I come to the office? | a constraint the applicant stated in turn 6 and never repeated | Thursday | retrieved | You can come to the office on **Thursdays**. |
| Q-5 | What did I ask you about my employer? | an open question, turn 7, never answered | letter / employer | retrieved | You asked whether a **scanned letter from your employer is accepted or whether the original is required**. |

**Probes retrieved: 5/5**

### State object produced by compression

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
