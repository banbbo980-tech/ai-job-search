---
framework_version: 1.0.0
---

# Application Form Fields

Use this reference when an application portal asks for text beyond the CV and
cover letter: self-introductions, motivation or competency answers, project
entries, or fields with hard word or character limits.

## Grounding Rule

Every claim must be supported by at least one verified local source: the ignored
candidate profile overlay under `documents/cv/codex_profile/`, a source document
under `documents/`, the master example CV only where it still contains verified
candidate content, or a fact the user explicitly confirmed in the current task.
Tracked placeholder references and earlier generated drafts are not evidence.
Never add a claim merely to fill a field.

## Field Types

### Self-Introduction

For a 100-200 word paragraph, lead with the strongest relevant evidence, state
current status accurately, connect the candidate's trajectory to the role, and
finish with a verified employer-specific reason. Produce role-specific versions,
state the measured word count, and identify the first safe cut for a shorter form.

### Structured Project Entry

Use a descriptive project name, the candidate's actual role on the project, and
project dates only when those dates are known. Do not substitute employment dates
for unknown project dates. In 100-150 words, describe the system and users, the
candidate's scoped contribution, the hard problem, and a verified result. Also
provide a roughly 60-word version.

### Hard Character Limit

Prefer a concrete verified situation, number, or unusual background combination
over adjectives. Draft several angles, count characters programmatically, label
each count, and recommend one. Never estimate the count.

## Output

Save one ignored plain-text artifact beside the application materials:

`documents/applications/<company>_<role>/application_form_fields.txt`

Include field labels, measured counts, short variants, date references, and
clearly marked `NOTE TO SELF` blocks that are not for submission.

## Verification

- Trace every factual claim to verified evidence.
- Keep ownership and contribution scope exact.
- Keep dates consistent with the CV and cover letter.
- Describe in-progress qualifications as in progress.
- Measure word and character counts.
- Keep internal notes visibly separate from paste-ready text.
