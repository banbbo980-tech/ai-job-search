---
name: reset-job-profile
description: Confirmation-gated Codex reset workflow for candidate profile data and documents. Use for reset profile, reset documents, start over, clear candidate data, or wipe local career documents while preserving framework rules, templates, folder structure, and safety prompts.
---

# Reset Job Profile

This workflow is destructive. Nothing is deleted or cleared until the user types
the exact confirmation text `RESET`.

## Scopes

- `profile` clears candidate data from Codex profile references only.
- `documents` deletes user-provided files from `documents/` subfolders only.
- `all` does both.

If no valid scope is provided, ask the user to choose one of those exact scopes.

## Pre-Confirmation Report

Before changing anything, show what will be affected.

For `profile`, inspect:

- `documents/cv/codex_profile/01-candidate-profile.md`
- `documents/cv/codex_profile/02-behavioral-profile.md`
- `documents/cv/codex_profile/profile-summary.md`
- `documents/cv/codex_profile/search-preferences.md`
- `../job-application-core/references/01-candidate-profile.md`
- `../job-application-core/references/02-behavioral-profile.md`
- `../job-application-core/references/04-job-evaluation.md` personalized
  match areas, career goals, motivation, and life-situation placeholders
- `../job-application-core/references/05-cv-templates.md` profile statement area
- `../job-application-core/references/07-interview-prep.md` STAR examples and
  STAR candidates
- `../job-application-core/references/search-queries.md` placeholder query
  structure, plus the ignored local `search-preferences.md`

State which have content and which are already blank. Explicitly state that
writing style, scoring rules, cover-letter rules, LaTeX templates, and portal
skills are preserved. Do not describe evaluation preferences or search
preferences as framework-only data; `$job-setup` can personalize those areas in
the ignored local overlay.

For `documents`, list files under:

- `documents/cv/`
- `documents/linkedin/`
- `documents/diplomas/`
- `documents/references/`
- `documents/postings/`
- `documents/applications/`

State that `documents/README.md` and folder structure are preserved.

## Confirmation

Ask:

`Type RESET (all caps) to confirm, or anything else to cancel.`

Proceed only if the response is exactly `RESET`. Otherwise stop and report that
nothing changed.

## Execution

For `profile`:

- Replace the ignored local overlay files `01-candidate-profile.md`,
  `02-behavioral-profile.md`, `profile-summary.md`, and
  `search-preferences.md` under `documents/cv/codex_profile/` with blank
  templates or remove their personal content.
- Restore only the personalized placeholder values in
  `04-job-evaluation.md`; preserve the Eligibility Gate, Language Gate, scoring
  dimensions, Company Research Cache, and salary benchmark rules.
- Clear only profile statement templates in `05-cv-templates.md`.
- Clear ready-made STAR examples and STAR candidate stubs in
  `07-interview-prep.md`.
- Restore personalized role, skill, location, language, and portal query values
  in `search-queries.md` to placeholders if any were added outside the ignored
  local overlay.
- Leave framework rules intact.

For `documents`:

- Delete contents inside the personal document subfolders.
- Do not delete the folders or `documents/README.md`.
- Use safe path handling and verify the target is inside this repository before
  any recursive delete.

## Final Report

List what was cleared, what was already empty, and what was intentionally
preserved. Suggest `$job-setup` as the next step.
