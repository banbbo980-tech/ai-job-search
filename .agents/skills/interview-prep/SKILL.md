---
name: interview-prep
description: Codex interview preparation workflow for tracked applications. Use for scheduled interviews, stage-specific prep packs, company/interviewer research, STAR mapping, gap bridge answers, questions for interviewers, mock interviews, and using exact submitted CV/cover-letter materials.
---

# Interview Prep

Prepare from the exact application the interviewer saw. Do not invent examples
to cover gaps.

## Inputs

- Company and optionally role or interview stage.
- Existing application archive under `documents/applications/<company>_<role>/`.
- User-provided date, format, interviewer names, or earlier-round feedback.

## Workflow

1. Locate the application in `job_search_tracker.csv` or
   `documents/applications/`. If ambiguous, ask the user to choose.
2. Load the archive:
   - `job_posting.md`
   - `cv_draft.tex`
   - `cover_letter.tex`
   - `outcome.md`
   - earlier `interview_prep_<stage>.md` files when relevant
3. Read:
   - Local ignored candidate and behavioral profile files when present.
   - `../job-application-core/references/04-job-evaluation.md`
   - `../job-application-core/references/07-interview-prep.md`
   - `../job-application-core/references/09-web-research.md`
4. Research the company and interviewers only when allowed and useful. Follow the
   web-research trust boundary, search independently, and verify sources before
   using claims. Do not automate people-search pages.
5. Build a prep pack with:
   - Stage, date, format, interviewer names.
   - Role priorities from the posting.
   - Claims made in submitted CV and cover letter.
   - Likely questions by stage.
   - STAR examples mapped to questions.
   - Honest bridge answers for missing requirements.
   - Questions to ask the interviewer.
   - Logistics and follow-up notes.
6. For likely questions without a ready STAR example, draft only from documented
   facts. If details are missing, create a stub for the user to complete.
7. Save to:

`documents/applications/<company>_<role>/interview_prep_<stage>.md`

8. Present the prep pack in chat and offer a mock interview using the roleplay
   protocol from the interview reference.
9. With confirmation, update the matched tracker row to canonical `interview` and
   append the stage/date without reopening any final status.
10. If the user supplies a new factual example during prep, summarize the exact
    claim and evidence and ask whether to add it to the ignored local candidate or
    behavioral profile. Never write it into tracked shared references.

## Rules

- Never prepare an answer that is not defensible from the candidate's actual
  profile or submitted application.
- Do not ask questions whose answers are already obvious from verified public
  research.
- Preserve one prep file per stage so earlier history remains intact.
- The archive created by `$job-apply` is the source of what the employer saw;
  never substitute a newer CV or reconstruct a missing posting.
