# Sublab Hard - results

## Part 1 - extraction

| Story | Parsed | Valid | Null fields | Traps hit |
|---|---|---|---|---|
| story-01 | yes | yes | none | none |
| story-02 | yes | yes | graduation_year, gpa_4_scale, gpa_original_scale, experience_months | no GPA / GPA not clear -> null; contradiction: Experience months are not countable because the story gives "thirty-six months" but does not provide a written start month and end month; it says the employment is "continuing today". |
| story-03 | yes | yes | none | GPA on 5.0 scale -> converted to 3.68; 1 not published, not counted |
| story-04 | yes | yes | none | 3 not published, not counted |
| story-05 | yes | yes | none | 1 not published, not counted |
| story-06 | yes | yes | degree, graduation_year, gpa_4_scale, gpa_original_scale, experience_months | no GPA / GPA not clear -> null; 1 not published, not counted; contradiction: The story says both "I graduated in 2024 with a BSc in Statistics" and "I am currently a final-year student graduating in 2026," so degree and graduation year are contradictory.; contradiction: The GPA is stated as both 3.2 and 3.5, so it cannot be resolved; no grading scale is stated.; contradiction: Experience has a written start month (February 2023) but no written end month; "about forty months" and the ongoing wording are not countable under the rules. |

## Part 2 - scores (model) and total (code)

| Rank | Story | Name | Academic | Research | Experience | Total |
|---|---|---|---|---|---|---|
| 1 | story-01 | Aziza Bekova | 5 | 5 | 2 | 4.40 |
| 2 | story-04 | Tamerlan Saparov | 4 | 2.5 | 5 | 3.75 |
| 3 | story-05 | Аиша Нұрланқызы | 5 | 2.5 | 1.25 | 3.50 |
| 4 | story-03 | Lyazzat Omarova | 4 | 2.5 | 3 | 3.35 |
| 5 | story-02 | Dias Yerzhanov | 2.5 | 2.5 | 0 | 2.00 |
| 6 | story-06 | Nurzhan Abilov | 2 | 2.5 | 0 | 1.75 |

**Winner (computed in code): story-01 - Aziza Bekova, total 4.40**
Gap between #1 and #2: 0.65

## Part 2 - prose answer (separate call)

Aziza Bekova should receive the funded place.

She has the strongest overall evidence under the stated rules: a 3.8 GPA on a 4.0 scale, two published peer-reviewed outputs, and eight months of directly relevant work. Both publications count because the story explicitly says they were published; there is no need to count any merely submitted or planned work.

The closest alternatives are weaker in important respects. Aisha Nurlankyzy has a slightly higher GPA, but only one published paper and six months of experience. Tamerlan Saparov has 24 months of relevant work, but his GPA is 3.6 and only one of his four listed research items is published; the other three must not be counted. Lyazzat Omarova has a strong stated record—4.6/5.0, equivalent to 3.68/4.0—and 14 months of internships, but only one published paper. Dias Yerzhanov and Nurzhan Abilov have substantial work experience, but Dias provides no GPA and Nurzhan’s GPA is contradictory, so neither can receive a reliable academic score.

Using a reasonable intermediate scoring scheme—five for the stated top benchmark, half credit for one of two publications, and experience capped at five points at 24 months—Aziza ranks first with an illustrative weighted total of about 4.33/5. Her advantage in both academic record and published research outweighs her shorter work experience.

## Records

```json
{
  "story-01": {
    "candidate_id": "story-01",
    "full_name": "Aziza Bekova",
    "degree": "BSc in Computer Science",
    "graduation_year": 2025,
    "gpa_4_scale": 3.8,
    "gpa_original_scale": 4,
    "languages": [
      "Kazakh",
      "Russian",
      "English (C1)"
    ],
    "published_count": 2,
    "unpublished_outputs": [],
    "experience_months": 8,
    "evidence": {
      "candidate_id": "CANDIDATE ID: story-01",
      "full_name": "Aziza Bekova",
      "degree": "I completed my BSc in Computer Science in June 2025.",
      "graduation_year": "I completed my BSc in Computer Science in June 2025.",
      "gpa_4_scale": "My final GPA was 3.8 on a 4.0 scale.",
      "gpa_original_scale": "My final GPA was 3.8 on a 4.0 scale.",
      "languages": "I speak Kazakh and Russian fluently and my English is at C1.",
      "published_count": "Both are peer-reviewed publications.",
      "unpublished_outputs": "Both are peer-reviewed publications.",
      "experience_months": "from October 2023 to May 2024, eight months in total."
    },
    "contradictions": []
  },
  "story-02": {
    "candidate_id": "story-02",
    "full_name": "Dias Yerzhanov",
    "degree": "Bachelor's in Information Systems",
    "graduation_year": null,
    "gpa_4_scale": null,
    "gpa_original_scale": null,
    "languages": [
      "Kazakh",
      "Russian",
      "English (B2)"
    ],
    "published_count": 1,
    "unpublished_outputs": [],
    "experience_months": null,
    "evidence": {
      "candidate_id": "CANDIDATE ID: story-02",
      "full_name": "scholarship application - Dias Yerzhanov",
      "degree": "I finished my bachelor's in Information Systems last year with a diploma with distinction.",
      "graduation_year": "I finished my bachelor's in Information Systems last year with a diploma with distinction.",
      "gpa_4_scale": "There is no GPA figure anywhere in my transcript that I would want to put in a letter, so I am not going to make one up.",
      "gpa_original_scale": "There is no GPA figure anywhere in my transcript that I would want to put in a letter, so I am not going to make one up.",
      "languages": "Languages: Kazakh, Russian, English (B2).",
      "published_count": "On the research side I have one published paper, in a student conference proceedings, about the scheduling tool.",
      "unpublished_outputs": "On the research side I have one published paper, in a student conference proceedings, about the scheduling tool.",
      "experience_months": "I have been employed continuously for three years. That is thirty-six months as a backend developer at a logistics company, starting the month after my third year ended and continuing today.",
      "contradictions": "I have been employed continuously for three years. That is thirty-six months as a backend developer at a logistics company, starting the month after my third year ended and continuing today."
    },
    "contradictions": [
      "Experience months are not countable because the story gives \"thirty-six months\" but does not provide a written start month and end month; it says the employment is \"continuing today\"."
    ]
  },
  "story-03": {
    "candidate_id": "story-03",
    "full_name": "Lyazzat Omarova",
    "degree": "BSc in Applied Mathematics",
    "graduation_year": 2025,
    "gpa_4_scale": 3.68,
    "gpa_original_scale": 5.0,
    "languages": [
      "Kazakh",
      "Russian",
      "English"
    ],
    "published_count": 1,
    "unpublished_outputs": [
      "A second paper is under review at a journal since March 2026."
    ],
    "experience_months": 14,
    "evidence": {
      "candidate_id": "CANDIDATE ID: story-03",
      "full_name": "# Lyazzat Omarova — application notes",
      "degree": "BSc in Applied Mathematics, completed 2025.",
      "graduation_year": "BSc in Applied Mathematics, completed 2025.",
      "gpa_4_scale": "My GPA was 4.6 out of 5.0. I realise this is not the scale you asked for; I have not converted it because I did not want to present a number I had calculated myself.",
      "gpa_original_scale": "My GPA was 4.6 out of 5.0.",
      "languages": "Kazakh, Russian, English.",
      "published_count": "One paper published in 2024 in a peer-reviewed conference proceedings (graph theory, a small result, entirely mine).",
      "unpublished_outputs": "A second paper is under review at a journal since March 2026 — I am listing it for completeness and I understand it does not count as published.",
      "experience_months": "The first ran from June 2023 to February 2024, the second from March 2024 to July 2024."
    },
    "contradictions": []
  },
  "story-04": {
    "candidate_id": "story-04",
    "full_name": "Tamerlan Saparov",
    "degree": "BSc in Computer Science",
    "graduation_year": 2026,
    "gpa_4_scale": 3.6,
    "gpa_original_scale": 4.0,
    "languages": [
      "Kazakh",
      "Russian",
      "English",
      "Turkish (A2)"
    ],
    "published_count": 1,
    "unpublished_outputs": [
      "A survey of Kazakh NLP resources",
      "Tokenizers considered harmful",
      "Evaluation without annotation"
    ],
    "experience_months": 24,
    "evidence": {
      "candidate_id": "CANDIDATE ID: story-04",
      "full_name": "Tamerlan Saparov",
      "degree": "BSc in Computer Science",
      "graduation_year": "graduating 2026",
      "gpa_4_scale": "GPA 3.6 on a 4.0 scale.",
      "gpa_original_scale": "GPA 3.6 on a 4.0 scale.",
      "languages": "Kazakh, Russian, English, Turkish (A2).",
      "published_count": "So: one published, one under review, two in preparation.",
      "unpublished_outputs": "2. *A survey of Kazakh NLP resources*, submitted to a journal in January 2026. Under review.\n3. *Tokenizers considered harmful*, in preparation. Not submitted anywhere.\n4. *Evaluation without annotation*, in preparation. Also not submitted.",
      "experience_months": "from September 2023 to September 2025"
    },
    "contradictions": []
  },
  "story-05": {
    "candidate_id": "story-05",
    "full_name": "Аиша Нұрланқызы",
    "degree": "Информатика бакалавриаты",
    "graduation_year": 2025,
    "gpa_4_scale": 3.9,
    "gpa_original_scale": 4.0,
    "languages": [
      "қазақ",
      "орыс",
      "ағылшын (C1)"
    ],
    "published_count": 1,
    "unpublished_outputs": [
      "Тағы бір мақала жазылып жатыр, бірақ ол әлі еш жерге жіберілген жоқ."
    ],
    "experience_months": 6,
    "evidence": {
      "candidate_id": "CANDIDATE ID: story-05",
      "full_name": "Менің атым Аиша Нұрланқызы.",
      "degree": "2025 жылы информатика бакалавриатын бітірдім.",
      "graduation_year": "2025 жылы информатика бакалавриатын бітірдім.",
      "gpa_4_scale": "GPA-м 3.9 (4.0 шкаласы бойынша) — бұл менің транскриптімде жазылған сан.",
      "gpa_original_scale": "GPA-м 3.9 (4.0 шкаласы бойынша) — бұл менің транскриптімде жазылған сан.",
      "languages": "Тілдер: қазақ, орыс, ағылшын (C1).",
      "published_count": "2025 жылы рецензияланатын конференция жинағында бір мақалам жарияланды, деректер жиынтығының сапасы туралы еді.",
      "unpublished_outputs": "Тағы бір мақала жазылып жатыр, бірақ ол әлі еш жерге жіберілген жоқ.",
      "experience_months": "2025 жылдың қыркүйегінен 2026 жылдың ақпанына дейін бір компанияда алты ай тағылымдамадан өттім."
    },
    "contradictions": []
  },
  "story-06": {
    "candidate_id": "story-06",
    "full_name": "Nurzhan Abilov",
    "degree": null,
    "graduation_year": null,
    "gpa_4_scale": null,
    "gpa_original_scale": null,
    "languages": [
      "Kazakh",
      "Russian",
      "English"
    ],
    "published_count": 1,
    "unpublished_outputs": [
      "One poster at a local event"
    ],
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
}
```