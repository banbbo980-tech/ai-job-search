# AI Job Search Codex Guide

This repository is a local-first job-search and application workspace for OpenAI
Codex and ChatGPT Work. It helps a candidate build a profile, search and rank
jobs, generate tailored LaTeX CVs and cover letters, prepare for interviews,
record outcomes, and plan upskilling.

## Essential Rules

- Preserve the candidate's real history. Never invent experience, skills,
  credentials, achievements, dates, titles, salary data, references, or STAR
  examples.
- Treat personal materials as private local data. Do not expose documents,
  generated applications, tracker rows, salary data, API keys, or secrets.
- Evaluate job fit before drafting an application. If the workflow requires
  confirmation, stop after the fit evaluation and ask before writing CV or cover
  letter files.
- Keep the full application workflow intact: posting parse, fit evaluation,
  confirmation, tailored CV, tailored cover letter, independent review, revision,
  LaTeX compile, visual/layout inspection, ATS verification, and final checklist.
- Keep generated CVs and cover letters in LaTeX unless the user explicitly asks
  for a different output later.
- Keep the CV exactly two pages and the cover letter exactly one page when the
  selected template/workflow requires those limits.
- Preserve destructive-action gates. Reset and deletion workflows must display
  exactly what will change and require the exact confirmation text before acting.
- Preserve attribution to the original independent MIT-licensed project. Do not
  imply OpenAI created or endorses it.

## Codex Skills

Use these project skills from `.agents/skills/`:

- `$job-setup` for onboarding and profile refresh.
- `$job-search` for job portal searches, deduplication, and seen-job state.
- `$job-rank` for triage scoring scraped jobs.
- `$job-apply` for the full application package.
- `$profile-expand` for additive competency discovery.
- `$interview-prep` for stage-specific interview preparation.
- `$application-outcome` for tracker/archive updates.
- `$upskill-analysis` for skill-gap and learning-plan reports.
- `$add-document-template` for custom LaTeX templates.
- `$add-job-portal` for custom portal search skills.
- `$reset-job-profile` for confirmation-gated resets.
- `$job-application-core` for shared profile, writing, evaluation, template, and
  search-query references.

The legacy `CLAUDE.md` and `.claude/` tree are retained during migration for
history and parity comparison. Codex workflows should use the `.agents/skills/`
instructions and `.agents/skills/job-application-core/references/` as the active
Codex-native source.

## Shared Reference Files

Codex workflow skills should read only the references they need:

- `.agents/skills/job-application-core/references/01-candidate-profile.md`
- `.agents/skills/job-application-core/references/02-behavioral-profile.md`
- `.agents/skills/job-application-core/references/03-writing-style.md`
- `.agents/skills/job-application-core/references/04-job-evaluation.md`
- `.agents/skills/job-application-core/references/05-cv-templates.md`
- `.agents/skills/job-application-core/references/06-cover-letter-templates.md`
- `.agents/skills/job-application-core/references/07-interview-prep.md`
- `.agents/skills/job-application-core/references/search-queries.md`

## Verification Commands

Run the available checks after migration edits:

```bash
python -m unittest discover -s tests -t . -v
python tools/lint_skills.py
python tools/security_guards.py
python tools/codex_compatibility.py
```

For portal CLIs, use the project-standard Bun checks when Bun is installed:

```bash
cd .agents/skills/<portal-skill>/cli
bun install
bun run typecheck
bun test --timeout 30000
```

When Bun is unavailable, an npm-based typecheck may be used as a local fallback
for signal only, but CI and official verification remain Bun-based.

For document smoke tests when LaTeX is installed:

```bash
cd cv && lualatex -interaction=nonstopmode -halt-on-error main_example.tex
cd ../cover_letters && xelatex -interaction=nonstopmode -halt-on-error cover_example.tex
```

For ATS extraction when Poppler is installed:

```bash
pdftotext -layout cv/main_example.pdf cv/main_example.txt
```

If Bun, LaTeX, or `pdftotext` are unavailable locally, report those checks as
environment-blocked and preserve CI/documented coverage.

## Subagent Review

For `$job-apply`, Codex is the drafter. Delegate a separate reviewer subagent with
fresh context when subagents are available. Pass the exact posting, candidate
evidence, CV draft, and cover-letter draft inline or as explicit file paths. The
reviewer must check targeting, unsupported claims, missing supported keywords,
generic language, company alignment, and role alignment. The drafter must verify
reviewer recommendations before applying them.

If subagents are unavailable, run the documented second-pass reviewer fallback in
`$job-apply`: separate the review pass from drafting, reload the exact evidence,
and apply the same criteria without inventing facts.

## Repository Constraints

- Do not convert this project into a Node.js web app.
- Keep portal CLIs under `.agents/skills/<portal>/cli`.
- Keep personal files ignored by Git.
- Do not remove `CLAUDE.md` or `.claude/` until Codex parity tests pass.
- Do not install global software or change system-wide configuration without user
  approval.
