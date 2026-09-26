## Sublab Easy - role_prompts results

### policy_officer

| Enquiry | Parsed | Schema OK | found | decision | amount | missing_documents |
|---|---|---|---|---|---|---|
| E-01 | yes | yes | match | match | match | match |
| E-02 | yes | yes | match | match | match | match |
| E-03 | yes | yes | match | match | match | match |
| E-04 | yes | yes | match | match | match | match |
| E-05 | yes | yes | match | match | match | match |
| E-06 | yes | yes | match | match | match | match |
| E-07 | yes | yes | match | match | match | match |
| E-08 | yes | yes | match | match | match | match |
| E-09 | yes | yes | match | match | match | match |
| E-10 | yes | yes | match | match | match | match |

### front_desk

| Enquiry | Parsed | Schema OK | found | decision | amount | missing_documents |
|---|---|---|---|---|---|---|
| E-01 | yes | yes | match | match | match | match |
| E-02 | yes | yes | match | match | match | match |
| E-03 | yes | yes | match | MOVED | match | match |
| E-04 | yes | yes | match | MOVED | match | match |
| E-05 | yes | yes | match | match | match | match |
| E-06 | yes | yes | match | match | match | match |
| E-07 | yes | yes | match | match | match | match |
| E-08 | yes | yes | match | match | match | match |
| E-09 | yes | yes | match | MOVED | match | match |
| E-10 | yes | yes | match | match | match | match |

### auditor

| Enquiry | Parsed | Schema OK | found | decision | amount | missing_documents |
|---|---|---|---|---|---|---|
| E-01 | yes | yes | match | MOVED | MOVED | match |
| E-02 | yes | yes | match | match | match | match |
| E-03 | yes | yes | match | MOVED | match | match |
| E-04 | yes | yes | match | MOVED | match | match |
| E-05 | yes | yes | match | MOVED | MOVED | match |
| E-06 | yes | yes | match | MOVED | MOVED | match |
| E-07 | yes | yes | match | MOVED | MOVED | match |
| E-08 | yes | yes | match | match | match | match |
| E-09 | yes | yes | match | MOVED | match | match |
| E-10 | yes | yes | match | match | match | match |

### bilingual_clerk

| Enquiry | Parsed | Schema OK | found | decision | amount | missing_documents |
|---|---|---|---|---|---|---|
| E-01 | yes | yes | match | match | match | match |
| E-02 | yes | yes | match | match | match | match |
| E-03 | yes | yes | match | match | match | match |
| E-04 | yes | yes | match | match | match | match |
| E-05 | yes | yes | match | match | match | match |
| E-06 | yes | yes | match | match | match | match |
| E-07 | yes | yes | match | match | match | match |
| E-08 | yes | yes | match | match | match | match |
| E-09 | yes | yes | match | match | match | match |
| E-10 | yes | yes | match | match | match | match |

### Field movement vs policy_officer

| Role | Field | Enquiries moved |
|---|---|---|
| front_desk | found | (none) |
| front_desk | decision | E-03, E-04, E-09 |
| front_desk | amount | (none) |
| front_desk | missing_documents | (none) |
| auditor | found | (none) |
| auditor | decision | E-01, E-03, E-04, E-05, E-06, E-07, E-09 |
| auditor | amount | E-01, E-05, E-06, E-07 |
| auditor | missing_documents | (none) |
| bilingual_clerk | found | (none) |
| bilingual_clerk | decision | (none) |
| bilingual_clerk | amount | (none) |
| bilingual_clerk | missing_documents | (none) |

### Raw replies (for transcripts)

#### policy_officer
- **E-01**: `{
  "applicant_id": "A-201",
  "found": true,
  "decision": "granted",
  "amount": 250000,
  "missing_documents": [],
  "reason": "GPA 3.4 and income band 1, with both documents on file."
}`
- **E-02**: `{
  "applicant_id": "A-202",
  "found": true,
  "decision": "more_info",
  "amount": 0,
  "missing_documents": ["id_card"],
  "reason": "GPA 2.9 and income band 2 meet the policy requirements. The transcript is on file, but the id_card is missing."
}`
- **E-03**: `{
  "applicant_id": "A-203",
  "found": true,
  "decision": "refused",
  "amount": 0,
  "missing_documents": [],
  "reason": "GPA 2.4 is below the minimum 2.67; income band 1 is allowed, and both required documents are on file."
}`
- **E-04**: `{
  "applicant_id": "A-204",
  "found": true,
  "decision": "refused",
  "amount": 0,
  "missing_documents": [],
  "reason": "GPA 3.1 meets the minimum of 2.67 and both documents are on file, but income band 3 is not among the allowed bands 1 or 2."
}`
- **E-05**: `{
  "applicant_id": "A-205",
  "found": true,
  "decision": "granted",
  "amount": 250000,
  "missing_documents": [],
  "reason": "GPA 3.7 and income band 1, with both required documents on file."
}`
- **E-06**: `{
  "applicant_id": "A-206",
  "found": true,
  "decision": "granted",
  "amount": 150000,
  "missing_documents": [],
  "reason": "GPA 2.7 and income band 2, with both transcript and id_card on file."
}`
- **E-07**: `{
  "applicant_id": "A-201",
  "found": true,
  "decision": "granted",
  "amount": 250000,
  "missing_documents": [],
  "reason": "GPA 3.4 and income band 1, with both required documents on file."
}`
- **E-08**: `{
  "applicant_id": "A-999",
  "found": false,
  "decision": "not_found",
  "amount": 0,
  "missing_documents": [],
  "reason": "No record matches applicant ID A-999 or the name Bekzat Nurly."
}`
- **E-09**: `{
  "applicant_id": "A-203",
  "found": true,
  "decision": "refused",
  "amount": 0,
  "missing_documents": [],
  "reason": "GPA 2.4 is below the minimum of 2.67; income band 1 is allowed, and both transcript and id_card are on file."
}`
- **E-10**: `{
  "applicant_id": "A-202",
  "found": true,
  "decision": "more_info",
  "amount": 0,
  "missing_documents": [
    "id_card"
  ],
  "reason": "GPA 2.9 and income band 2 meet the policy requirements; transcript is on file, but id_card is missing."
}`

#### front_desk
- **E-01**: `{
  "applicant_id": "A-201",
  "found": true,
  "decision": "granted",
  "amount": 250000,
  "missing_documents": [],
  "reason": "GPA 3.4 and income band 1, with both documents on file."
}`
- **E-02**: `{
  "applicant_id": "A-202",
  "found": true,
  "decision": "more_info",
  "amount": 0,
  "missing_documents": [
    "id_card"
  ],
  "reason": "Your GPA is 2.9 and income band 2 meet the policy thresholds. Please provide the missing id card so the office can revisit your application."
}`
- **E-03**: `{
  "applicant_id": "A-203",
  "found": true,
  "decision": "more_info",
  "amount": 0,
  "missing_documents": [],
  "reason": "Your transcript and id card are on file, and income band 1 is eligible. However, the recorded GPA is 2.4, below the required minimum of 2.67. The GPA would need to meet or exceed 2.67 before the office can revisit the application."
}`
- **E-04**: `{
  "applicant_id": "A-204",
  "found": true,
  "decision": "more_info",
  "amount": 0,
  "missing_documents": [],
  "reason": "Your GPA is 3.1 and both required documents are on file, but income band 3 is not currently eligible under the policy. The grant can be reconsidered if your recorded income band changes to 1 or 2."
}`
- **E-05**: `{
  "applicant_id": "A-205",
  "found": true,
  "decision": "granted",
  "amount": 250000,
  "missing_documents": [],
  "reason": "GPA 3.7 and income band 1 meet the policy requirements, with both the transcript and id card on file."
}`
- **E-06**: `{
  "applicant_id": "A-206",
  "found": true,
  "decision": "granted",
  "amount": 150000,
  "missing_documents": [],
  "reason": "GPA 2.7 and income band 2 meet the policy requirements, with both required documents on file."
}`
- **E-07**: `{
  "applicant_id": "A-201",
  "found": true,
  "decision": "granted",
  "amount": 250000,
  "missing_documents": [],
  "reason": "GPA 3.4 and income band 1 meet the policy requirements, with both required documents on file."
}`
- **E-08**: `{
  "applicant_id": "A-999",
  "found": false,
  "decision": "not_found",
  "amount": 0,
  "missing_documents": [],
  "reason": "No applicant record matches ID A-999 or the name Bekzat Nurly."
}`
- **E-09**: `{
  "applicant_id": "A-203",
  "found": true,
  "decision": "more_info",
  "amount": 0,
  "missing_documents": [],
  "reason": "Your transcript and ID card are on file, and your income band is eligible. However, your GPA is 2.4, below the required minimum of 2.67. You would need to meet the GPA threshold before the office can revisit your application."
}`
- **E-10**: `{
  "applicant_id": "A-202",
  "found": true,
  "decision": "more_info",
  "amount": 0,
  "missing_documents": [
    "id_card"
  ],
  "reason": "Your GPA of 2.9 and income band 2 meet the policy thresholds, but the id card is not yet on file. Please provide the id card so the office can revisit your application."
}`

#### auditor
- **E-01**: `{
  "applicant_id": "A-201",
  "found": true,
  "decision": "more_info",
  "amount": 0,
  "missing_documents": [],
  "reason": "The file meets the criteria on a first reading: GPA 3.4 meets the minimum threshold of 2.67, income band 1 is allowed, and both required documents are on file. It is queued for a second reader before any money moves."
}`
- **E-02**: `{
  "applicant_id": "A-202",
  "found": true,
  "decision": "more_info",
  "amount": 0,
  "missing_documents": [
    "id_card"
  ],
  "reason": "The file meets the GPA threshold (2.9 is at least 2.67) and the allowed income-band rule (band 2), but the required id_card is missing. It is queued for a second reader."
}`
- **E-03**: `{
  "applicant_id": "A-203",
  "found": true,
  "decision": "more_info",
  "amount": 0,
  "missing_documents": [],
  "reason": "GPA 2.4 is below the required minimum of 2.67. The file requires a second reader regardless of outcome."
}`
- **E-04**: `{
  "applicant_id": "A-204",
  "found": true,
  "decision": "more_info",
  "amount": 0,
  "missing_documents": [],
  "reason": "The file requires a second reader. GPA 3.1 meets the 2.67 threshold and both required documents are on file, but income band 3 is not an allowed band; policy allows only income bands 1 or 2."
}`
- **E-05**: `{
  "applicant_id": "A-205",
  "found": true,
  "decision": "more_info",
  "amount": 0,
  "missing_documents": [],
  "reason": "The file meets the criteria on a first reading: GPA 3.7 meets the minimum threshold of 2.67, income band 1 is allowed, and both required documents (transcript and id_card) are on file. It is queued for a second reader."
}`
- **E-06**: `{
  "applicant_id": "A-206",
  "found": true,
  "decision": "more_info",
  "amount": 0,
  "missing_documents": [],
  "reason": "The file meets the criteria on a first reading: GPA 2.7 meets the 2.67 threshold, income band 2 is allowed, and both the transcript and id_card are on file. Queued for a second reader."
}`
- **E-07**: `{
  "applicant_id": "A-201",
  "found": true,
  "decision": "more_info",
  "amount": 0,
  "missing_documents": [],
  "reason": "The file meets the criteria on a first reading: GPA 3.4 meets the minimum threshold of 2.67, income band 1 is allowed, and both required documents are on file. Queued for a second reader before any money moves."
}`
- **E-08**: `{
  "applicant_id": "A-999",
  "found": false,
  "decision": "not_found",
  "amount": 0,
  "missing_documents": [],
  "reason": "No matching applicant was found by applicant ID, name, or Kazakh-script alias in RECORDS."
}`
- **E-09**: `{
  "applicant_id": "A-203",
  "found": true,
  "decision": "more_info",
  "amount": 0,
  "missing_documents": [],
  "reason": "The file is queued for a second reader because the GPA is 2.4, below the required minimum of 2.67; income band 1 and both required documents are on file."
}`
- **E-10**: `{
  "applicant_id": "A-202",
  "found": true,
  "decision": "more_info",
  "amount": 0,
  "missing_documents": ["id_card"],
  "reason": "The record shows GPA 2.9 and allowed income band 2, but the required id_card is not on file. The file requires a second reader."
}`

#### bilingual_clerk
- **E-01**: `{
  "applicant_id": "A-201",
  "found": true,
  "decision": "granted",
  "amount": 250000,
  "missing_documents": [],
  "reason": "GPA 3.4 meets the minimum, income band 1 is eligible, and both required documents are on file."
}`
- **E-02**: `{
  "applicant_id": "A-202",
  "found": true,
  "decision": "more_info",
  "amount": 0,
  "missing_documents": ["id_card"],
  "reason": "The applicant meets the GPA and income requirements but still needs to provide the id card."
}`
- **E-03**: `{
  "applicant_id": "A-203",
  "found": true,
  "decision": "refused",
  "amount": 0,
  "missing_documents": [],
  "reason": "The application is refused because the GPA is 2.4, below the minimum required GPA of 2.67."
}`
- **E-04**: `{
  "applicant_id": "A-204",
  "found": true,
  "decision": "refused",
  "amount": 0,
  "missing_documents": [],
  "reason": "GPA 3.1 meets the minimum, but income band 3 is not an allowed band."
}`
- **E-05**: `{
  "applicant_id": "A-205",
  "found": true,
  "decision": "granted",
  "amount": 250000,
  "missing_documents": [],
  "reason": "GPA 3.7 and income band 1 meet the requirements, with both required documents on file."
}`
- **E-06**: `{
  "applicant_id": "A-206",
  "found": true,
  "decision": "granted",
  "amount": 150000,
  "missing_documents": [],
  "reason": "GPA 2.7 and income band 2 meet the requirements, with both required documents on file."
}`
- **E-07**: `{
  "applicant_id": "A-201",
  "found": true,
  "decision": "granted",
  "amount": 250000,
  "missing_documents": [],
  "reason": "GPA 3.4 және табыс санаты 1, транскрипт пен жеке куәлік құжаттары толық бар."
}`
- **E-08**: `{
  "applicant_id": "A-999",
  "found": false,
  "decision": "not_found",
  "amount": 0,
  "missing_documents": [],
  "reason": "Applicant ID A-999 and the name Bekzat Nurly were not found in the records."
}`
- **E-09**: `{
  "applicant_id": "A-203",
  "found": true,
  "decision": "refused",
  "amount": 0,
  "missing_documents": [],
  "reason": "GPA 2.4 is below the minimum required GPA of 2.67."
}`
- **E-10**: `{
  "applicant_id": "A-202",
  "found": true,
  "decision": "more_info",
  "amount": 0,
  "missing_documents": ["id_card"],
  "reason": "The record shows GPA 2.9 and income band 2, but the id card is missing from the documents on file."
}`
