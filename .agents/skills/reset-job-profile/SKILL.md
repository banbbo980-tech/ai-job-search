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

- `../job-application-core/references/01-candidate-profile.md`
- `../job-application-core/references/02-behavioral-profile.md`
- `../job-application-core/references/05-cv-templates.md` profile statement area
- `../job-application-core/references/07-interview-prep.md` STAR examples and
  STAR candidates

State which have content and which are already blank. Explicitly state that
writing style, evaluation rules, cover-letter rules, LaTeX templates, and portal
skills are preserved.

For `documents`, list files under:

- `documents/cv/`
- `documents/linkedin/`
- `documents/diplomas/`
- `documents/references/`
- `documents/applications/`

State that `documents/README.md` and folder structure are preserved.

## Confirmation

Ask:

`Type RESET (all caps) to confirm, or anything else to cancel.`

Proceed only if the response is exactly `RESET`. Otherwise stop and report that
nothing changed.

## Execution

For `profile`:

- Replace `01-candidate-profile.md` with a blank structured template.
- Replace `02-behavioral-profile.md` with a blank structured template.
- Clear only profile statement templates in `05-cv-templates.md`.
- Clear ready-made STAR examples and STAR candidate stubs in
  `07-interview-prep.md`.
- Leave framework rules intact.

For `documents`:

- Delete contents inside the personal document subfolders.
- Do not delete the folders or `documents/README.md`.
- Use safe path handling and verify the target is inside this repository before
  any recursive delete.

## Final Report

List what was cleared, what was already empty, and what was intentionally
preserved. Suggest `$job-setup` as the next step.
