---
name: job-setup
description: Codex onboarding workflow for the AI Job Search project. Use for initial candidate setup, rerunning setup after adding documents, importing a pasted CV, interview-style profile collection, or updating one section such as skills, experience, behavioral profile, STAR examples, or search configuration.
---

# Job Setup

Build or refresh the candidate profile without inventing facts. The workflow is
idempotent and privacy-first: real profile data is written only to the ignored
local overlay under `documents/cv/codex_profile/`.

## Inputs

- Optional section argument, e.g. `--section search`, `--section skills`, or
  `--section experience`.
- Documents under `documents/cv/`, `documents/linkedin/`, `documents/diplomas/`,
  `documents/references/`, and `documents/applications/`.
- A pasted or attached CV/resume.
- User answers from interview-style onboarding.

## Active Outputs

- `documents/cv/codex_profile/01-candidate-profile.md`
- `documents/cv/codex_profile/02-behavioral-profile.md`
- `documents/cv/codex_profile/profile-summary.md`
- `documents/cv/codex_profile/search-preferences.md`

Before any write, run `git ls-files --error-unmatch` and `git check-ignore -v`
for every target. Stop if a target is tracked or not ignored. Never place personal
facts in tracked shared references, `AGENTS.md`, `CLAUDE.md`, example documents,
tests, or public documentation.

Before the setup interview, inspect `git remote get-url origin`. If it is a
public GitHub fork or visibility cannot be confirmed, warn the user that pushes
are public and ask whether to continue with the verified ignored local overlay.
This check happens before any personal-data write. Never suggest force-adding the
overlay; use a separate private repository only when the user needs personal data
stored remotely.

## Workflow

1. Inspect `documents/` before greeting the user. Report files found in each
   expected subfolder.
2. Offer the three setup paths:
   - Path A: read the documents folder.
   - Path B: import one pasted or attached CV/resume.
   - Path C: conduct an interview-style setup.
3. For `--section <name>`, skip path selection and update only that section.
4. Read the local profile overlay first and the tracked shared references only as
   blank structure/rules. Use current local state to avoid duplicates and detect
   conflicts.
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
10. Fill remaining gaps one question at a time: career goals, target roles,
    location constraints, work authorization, deal-breakers, writing style, STAR
    examples, professional languages with honest levels, preferred CV language,
    and search configuration.
11. Discover portal skills under `.agents/skills/`. Explain that LinkedIn and
    Freehire are enabled defaults and Danish examples may have `enabled: false`.
    Enable or disable only the frontmatter toggle, and only after the user chooses
    the relevant markets. Suggest `$add-job-portal` for another public board.
12. Update the ignored local `search-preferences.md`; never personalize the
    tracked `references/search-queries.md` template.
13. Summarize files changed, unresolved conflicts, gaps left for the user, and
    suggested next skills: `$job-search` and `$job-apply`.

## Section Updates

For `--section search`, update only local `search-preferences.md`. Suggest role
types based on the complete verified profile, but let the user accept or reject
them. Record each query category in every professional language the user selected.

For STAR examples, draft only from actual experience. If the evidence is thin,
create STAR candidate stubs for the user to complete rather than fabricating a
result.

## Validation

- Every new claim must trace to a document, user answer, or cited public source.
- Inferred behavioral or writing-style observations must be labeled as inferred.
- Existing valid content must not be overwritten without explicit confirmation.
- Personal documents and generated profile details must remain ignored and
  untracked. Re-run `git check-ignore` and `git status --short` after writing.
