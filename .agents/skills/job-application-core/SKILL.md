---
name: job-application-core
description: Shared Codex-native reference bundle for the AI Job Search workspace. Use when a workflow needs privacy-safe profile resolution, writing and evaluation rules, document templates, interview guidance, application-form rules, web-research policy, or search configuration.
---

# Job Application Core

This skill is the shared reference layer for the Codex migration. It is not a
user workflow by itself; load it when another workflow needs profile, evaluation,
writing, template, search, or interview rules.

## Privacy-Safe Profile Resolution

Tracked files in `references/` are reusable framework templates. Real candidate
facts belong only in the ignored local overlay:

- `documents/cv/codex_profile/01-candidate-profile.md`
- `documents/cv/codex_profile/02-behavioral-profile.md`
- `documents/cv/codex_profile/profile-summary.md`
- `documents/cv/codex_profile/search-preferences.md`

For candidate facts, behavioral evidence, or search preferences, read the local
overlay first. Fall back to the corresponding tracked reference only when the
local file is absent, and treat placeholder text as missing data. Never write
personal facts into tracked references, `AGENTS.md`, `CLAUDE.md`, examples,
tests, or public documentation.

## Canonical References

Use these files as the active Codex references:

- `references/01-candidate-profile.md` - identity, education, experience, skills,
  references, and evidence.
- `references/02-behavioral-profile.md` - working style, strengths, preferences,
  and behavioral cautions.
- `references/03-writing-style.md` - prose, tone, and verification rules.
- `references/04-job-evaluation.md` - scoring dimensions, weights, verdict bands,
  deal-breakers, company research checklist, and recommendation format.
- `references/05-cv-templates.md` - LaTeX CV structure, tailoring rules,
  two-page enforcement, cuts, and ATS guidance.
- `references/06-cover-letter-templates.md` - LaTeX cover-letter structure,
  one-page enforcement, font pitfalls, and style rules.
- `references/07-interview-prep.md` - STAR examples, bridge answers, questions,
  mock-interview protocol, and follow-up guidance.
- `references/08-application-forms.md` - grounded portal text fields, measured
  character limits, project entries, and verification rules.
- `references/09-web-research.md` - posting trust boundary, ethical access
  escalation, robots policy, canonical-source preference, and claim verification.
- `references/search-queries.md` - portal list, role queries, location filters,
  and recency rules for `$job-search`.

## Compatibility Rule

The legacy `CLAUDE.md` and `.claude/` files remain in the repository during the
migration. They are historical/parity references, not the active Codex workflow
entry points. When creating or updating Codex workflows, point to the references
above rather than introducing new active dependencies on `.claude/`.

## Privacy Rule

Do not personalize the tracked references. Store real profile data in the ignored
local overlay above, never expose it outside the local project, and use fictional
data in tests and documentation.
