---
name: job-application-core
description: Shared Codex-native reference bundle for the AI Job Search workspace. Use when any job-search workflow needs the canonical candidate profile, behavioral profile, writing style, job evaluation framework, CV template rules, cover-letter template rules, interview framework, or search-query configuration.
---

# Job Application Core

This skill is the shared reference layer for the Codex migration. It is not a
user workflow by itself; load it when another workflow needs profile, evaluation,
writing, template, search, or interview rules.

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
- `references/search-queries.md` - portal list, role queries, location filters,
  and recency rules for `$job-search`.

## Compatibility Rule

The legacy `CLAUDE.md` and `.claude/` files remain in the repository during the
migration. They are historical/parity references, not the active Codex workflow
entry points. When creating or updating Codex workflows, point to the references
above rather than introducing new active dependencies on `.claude/`.

## Privacy Rule

These references may become personalized in a user's fork. Do not expose their
contents outside the local project. Do not add real personal data to test fixtures
or documentation.
