# Codex Migration Baseline

This baseline was captured before behavior-changing Codex migration edits.

Baseline source:

- Repository: `https://github.com/MadsLorentzen/ai-job-search`
- Branch: `upstream/master`
- Commit: `c134eef refactor(salary): optimize search match scoring and normalize Excel category keys (#101)`
- Local migration branch: `codex-migration`

## Environment

| Dependency | Check | Result |
|---|---|---|
| Python | `python --version` | Pass: `Python 3.14.2` |
| PyYAML | `python tools/lint_skills.py` import path | Pass: lint ran successfully |
| Node.js | `node --version` | Pass: `v24.15.0` |
| npm | `npm --version` | Pass: `11.12.1` |
| Bun | `bun --version` | Blocked locally: executable not on PATH |
| lualatex | `lualatex --version` | Blocked locally: executable not on PATH |
| xelatex | `xelatex --version` | Blocked locally: executable not on PATH |
| pdftotext | `pdftotext -v` | Blocked locally: executable not on PATH |

## Baseline Commands

| Area | Command | Result |
|---|---|---|
| Python unit tests | `python -m unittest discover -s tests -t . -v` | Pass: 60 tests ran, 60 passed |
| Skill/command lint | `python tools/lint_skills.py` | Pass: `lint_skills: OK (9 skills, 9 commands, settings.json)` |
| Security guards | `python tools/security_guards.py` | Pass: `security_guards: OK (permissions allowlist, gitignore rules, package manifests)` |
| Salary missing-data behavior | `python salary_lookup.py "Example Company" --json` | Expected graceful failure: `salary_data.json not found`, workflow should skip salary lookup |
| Salary converter help | `python tools/convert_salary_excel.py --help` | Pass: CLI help rendered |
| Portal TypeScript, alternate local check | `npm install --ignore-scripts --no-audit --fund=false && npm run typecheck` in each `.agents/skills/*/cli` directory | Pass for all six portal CLIs |

## Environment-Blocked Checks

The intended CI commands below were not run locally because the required
executables are not installed on PATH in this environment. Their CI coverage must
be preserved.

| Area | Intended command | Local status |
|---|---|---|
| Bun install/typecheck | `bun install` and `bun run typecheck` in each portal CLI directory | Blocked: Bun missing |
| Bun CLI tests | `bun test --timeout 30000` in each portal CLI directory | Blocked: Bun missing |
| CV LaTeX smoke | `cd cv && lualatex -interaction=nonstopmode main_example.tex` | Blocked: `lualatex` missing |
| Cover-letter LaTeX smoke | `cd cover_letters && xelatex -interaction=nonstopmode cover_example.tex` | Blocked: `xelatex` missing |
| ATS extraction smoke | `pdftotext -layout <cv.pdf> <cv.txt>` | Blocked: `pdftotext` missing and no local PDF compile |

## Representative Current Behavior

- `/setup` supports three onboarding paths: documents folder, pasted/imported CV, and interview mode.
- `/scrape` is implemented as a Claude skill trigger rather than a file under `.claude/commands/`.
- `/scrape` discovers portal CLI skills under `.agents/skills/*/SKILL.md`, uses Bun CLIs first, and falls back to web search when necessary.
- `/rank` batch-scores new jobs from `job_scraper/seen_jobs.json`, preserves scraper schema additively, applies deal-breaker vetoes, and marks expired jobs.
- `/apply` evaluates fit before drafting, asks for user confirmation, drafts LaTeX CV and cover letter, runs a separate reviewer agent, revises, compiles PDFs, inspects layout, checks ATS extraction, and reports a final checklist.
- `/interview` builds stage-specific prep from the archived submitted application and does not invent examples for gaps.
- `/outcome` updates the tracker and archive files, appending history without overwriting submitted artifacts.
- `/upskill` supports aggregate tracker analysis and targeted single-posting analysis.
- `/add-template` registers LaTeX templates only after capturing metadata and test-compiling.
- `/add-portal` scaffolds portal CLI skills after investigating public access, robots/terms constraints, and live query behavior.
- `/reset` requires exact `RESET` confirmation before destructive changes and preserves framework/template files.

## Pre-Existing Failures

No project test, lint, security, or TypeScript failures were observed in runnable
local checks. Local Bun, LaTeX, and `pdftotext` checks were environment-blocked,
not project failures.

## Baseline Caveats

- Live portal behavior was not tested during baseline because the repository's CI
  deliberately avoids automated live portal requests.
- The npm-based TypeScript check is an alternate local check only. The project
  remains Bun-based and CI should continue to use Bun.
- The audit clone generated ignored `node_modules/`, `package-lock.json`, and
  Python cache files during local validation. These are not part of the migration
  branch unless intentionally added later.
