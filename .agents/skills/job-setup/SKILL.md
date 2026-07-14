---
name: job-setup
description: Codex onboarding workflow for the AI Job Search project. Use for initial candidate setup, rerunning setup after adding documents, importing a pasted CV, interview-style profile collection, or updating one section such as skills, experience, behavioral profile, STAR examples, or search configuration.
---

# Job Setup

Build or refresh the candidate profile without inventing facts. This workflow is
idempotent: re-running it should add supported information, surface conflicts,
and preserve valid existing profile data.

## Inputs

- Optional section argument, e.g. `--section search`, `--section skills`, or
  `--section experience`.
- Documents under `documents/cv/`, `documents/linkedin/`, `documents/diplomas/`,
  `documents/references/`, and `documents/applications/`.
- A pasted or attached CV/resume.
- User answers from interview-style onboarding.

## Active Outputs

Update the Codex reference files under:

`../job-application-core/references/`

Also update root `AGENTS.md` only when durable repository workflow rules change.
Keep legacy `.claude/` files untouched unless the user explicitly asks for
legacy synchronization during the transition.

## Workflow

1. Inspect `documents/` before greeting the user. Report files found in each
   expected subfolder.
2. Offer the three setup paths:
   - Path A: read the documents folder.
   - Path B: import one pasted or attached CV/resume.
   - Path C: conduct an interview-style setup.
3. For `--section <name>`, skip path selection and update only that section.
4. Read the existing Codex reference files before extracting new data. Use that
   current state to avoid duplicates and detect conflicts.
5. Extract only evidence-backed facts:
   - CV: identity, contact, education, experience, skills, publications, awards.
   - LinkedIn: about text, experience, education, skills, certifications,
     volunteer work, publications, recommendations.
   - Diplomas: official degree titles, institutions, dates, grades if visible.
   - References: referee identity, relationship, exact competency language.
   - Application archives: postings, submitted drafts, outcomes, feedback.
6. Cross-check date, title, employer, education, and source conflicts. Do not
   choose silently when sources disagree.
7. Build a change set with two buckets:
   - Additive changes that do not touch existing content.
   - Conflicting changes requiring explicit user choice.
8. Present the full change set before writing. Ask the user to approve all,
   skip numbered items, or resolve conflicts.
9. Apply only confirmed changes with targeted edits. Do not rewrite whole files
   unless creating a blank template or replacing placeholder-only content.
10. Fill remaining gaps through concise follow-up questions: career goals,
    target roles, location constraints, deal-breakers, writing style, STAR
    examples, and search configuration. When asking about portals, explain that
    the project ships country-agnostic `linkedin-search` and `freehire-search`
    CLIs plus Danish portal examples, and that `$job-search` auto-discovers
    installed portal skills under `.agents/skills/`. If the user needs another
    local board, suggest `$add-job-portal`; web `site:` queries remain the
    fallback for portals without a CLI.
11. Update `references/search-queries.md` from the final search configuration.
12. Summarize files changed, unresolved conflicts, gaps left for the user, and
    suggested next skills: `$job-search` and `$job-apply`.

## Section Updates

For `--section search`, update only `references/search-queries.md` and the
search-related parts of the evaluation framework. Suggest role types based on
the complete profile, but let the user accept or reject them.

For STAR examples, draft only from actual experience. If the evidence is thin,
create STAR candidate stubs for the user to complete rather than fabricating a
result.

## Validation

- Every new claim must trace to a document, user answer, or cited public source.
- Inferred behavioral or writing-style observations must be labeled as inferred.
- Existing valid content must not be overwritten without explicit confirmation.
- Personal documents and generated profile details must remain local and must
  not be added to public docs or tests.
