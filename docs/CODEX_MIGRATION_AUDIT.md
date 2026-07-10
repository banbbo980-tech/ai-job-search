# Codex Migration Audit

This audit records the pre-migration state of the upstream `ai-job-search`
project before converting the active workflow from Claude Code to OpenAI Codex
and ChatGPT Work.

Audit source:

- Repository: `https://github.com/MadsLorentzen/ai-job-search`
- Upstream branch: `upstream/master`
- Local migration branch: `codex-migration`
- Baseline upstream commit: `c134eef refactor(salary): optimize search match scoring and normalize Excel category keys (#101)`

## Repository Shape

The upstream project is a job-application workspace with:

- Root Claude guidance in `CLAUDE.md`
- Claude command workflows in `.claude/commands/`
- Claude skills in `.claude/skills/`
- Portal Agent Skills and TypeScript CLIs in `.agents/skills/`
- LaTeX CV and cover-letter templates in `cv/` and `cover_letters/`
- Personal document input/output folders under `documents/`
- Job scraper state under `job_scraper/`
- Upskill report output under `upskill/`
- Python salary, lint, and security tooling under the root and `tools/`
- CI coverage in `.github/workflows/ci.yml`

## Migration Inventory

| Existing feature | Current entry point | Files involved | Claude-specific dependency | Codex replacement | Tests needed | Risk |
|---|---|---|---|---|---|---|
| Candidate setup | `/setup`, `/setup --section <name>` | `.claude/commands/setup.md`, `CLAUDE.md`, `.claude/skills/job-application-assistant/01-candidate-profile.md`, `02-behavioral-profile.md`, `03-writing-style.md`, `04-job-evaluation.md`, `05-cv-templates.md`, `06-cover-letter-templates.md`, `07-interview-prep.md`, `documents/README.md`, `cv/main_example.tex`, `.claude/skills/job-scraper/search-queries.md` | Claude slash command, `CLAUDE.md`, Claude Read/Edit/Write/Glob workflow language | `$job-setup` skill plus root `AGENTS.md` | Skill structure, setup paths, idempotent merge, confirmation before writes, sample profile output | High: personal data and profile merge behavior |
| Job searching/scraping | `/scrape` trigger through Claude skill | `.claude/skills/job-scraper/SKILL.md`, `.claude/skills/job-scraper/search-queries.md`, `.agents/skills/*`, `job_scraper/seen_jobs.json`, `job_search_tracker.csv` | Claude skill metadata and `Agent`/`WebSearch` wording | `$job-search` skill using existing portal CLIs and Codex/web fallback | Portal skill discovery, result normalization, dedup, seen state, tracker exclusion | High: live portal access and ToS/rate-limit behavior |
| Job ranking | `/rank` | `.claude/commands/rank.md`, `job_scraper/seen_jobs.json`, `job_search_tracker.csv`, `04-job-evaluation.md`, `01-candidate-profile.md` | Claude slash command and `general-purpose` Agent dispatch | `$job-rank` with Codex subagents or local chunk fallback | Ranking state updates, score weights, vetoes, expired jobs | Medium-high: subagent availability differs by environment |
| Fit evaluation | Part of `/apply` and `/rank` | `04-job-evaluation.md`, candidate profile files | Profile stored under Claude skill paths | Codex skills read migrated/shared profile and evaluation references | Strengths, gaps, transferables, deal-breakers, urgency, honest recommendation | High: scoring rules must not drift |
| Application generation | `/apply <url-or-text>` | `.claude/commands/apply.md`, job-application reference files, `cv/`, `cover_letters/`, `salary_lookup.py` | Claude slash command, Claude tool names, Claude Code-specific wording | `$job-apply` | Fit gate, draft CV, cover letter, reviewer, revision, compile, ATS, final checklist | High: complete user-facing workflow |
| Drafter-reviewer workflow | Internal to `/apply` | `.claude/commands/apply.md` | Claude `Agent` tool, `general-purpose` reviewer, Claude-specific tool constraints | Codex subagent reviewer with documented second-pass fallback | Reviewer independence, unsupported-claim detection, structured edits, verified company claims | High: critical quality and honesty mechanism |
| CV generation | `/apply`, `/add-template` | `cv/main_example.tex`, `05-cv-templates.md`, custom templates | Claude command references and `CLAUDE.md` checklist | `$job-apply`, `$add-document-template` | Exactly two pages where required, template activation, relevance-based cuts | High: LaTeX and layout-sensitive |
| Cover-letter generation | `/apply`, `/add-template` | `cover_letters/cover.cls`, `cover_letters/cover_example.tex`, `OpenFonts/`, `06-cover-letter-templates.md` | Claude command references | `$job-apply`, `$add-document-template` | Exactly one page, signature visible, fonts and bullet handling | High: LaTeX and visual layout |
| PDF compile and visual inspection | Internal to `/apply` | `cv/`, `cover_letters/`, LaTeX logs/PDFs | Claude Read tool on rendered PDFs | Codex PDF inspection where available; documented manual fallback when local rendering unavailable | Compile smoke, page counts, no clipped/orphaned content | High: environment-dependent |
| ATS checking | Internal to `/apply` | `pdftotext`, generated CV PDF/text | Claude command/checklist wording | Same `pdftotext` check, graceful reduced mode if unavailable | Extractable text, contact details, reading order, keyword honesty | Medium-high: optional local dependency |
| Interview preparation | `/interview` | `.claude/commands/interview.md`, `documents/applications/*`, `07-interview-prep.md`, profile/evaluation files | Claude slash command, WebSearch/WebFetch wording | `$interview-prep` | Uses exact submitted materials, company/interviewer research, STAR mapping, mock interview | Medium-high: depends on archives and web access |
| Outcome tracking | `/outcome` | `.claude/commands/outcome.md`, `job_search_tracker.csv`, `documents/applications/*` | Claude slash command | `$application-outcome` | Tracker row update, archive copy, `outcome.md` schema, no overwrite without confirmation | Medium |
| Profile expansion | `/expand` | `.claude/commands/expand.md`, documents folders, profile files | Claude slash command, web tool names | `$profile-expand` | Additive-only competency extraction, source tags, user confirmation | Medium |
| Upskill analysis | `/upskill`, `/upskill <URL>` | `.claude/skills/upskill/SKILL.md`, `job_search_tracker.csv`, profile files, `upskill/` | Claude skill metadata and WebSearch wording | `$upskill-analysis` | Aggregate and targeted modes, report naming, current resource lookup | Medium |
| Custom template registration | `/add-template` | `.claude/commands/add-template.md`, `templates/`, CV/letter template guidance | Claude slash command, Glob/Edit wording | `$add-document-template` | Manifest format, placeholder redaction, compile test, activation block | Medium-high |
| Custom portal generation | `/add-portal` | `.claude/commands/add-portal.md`, `.agents/skills/*` | Claude command, WebFetch/WebSearch, Bash examples | `$add-job-portal` | Portal investigation, robots/ToS handling, scaffold contract, live test | High: external access and generated code |
| Reset/start-over | `/reset` | `.claude/commands/reset.md`, profile files, `documents/*` | Claude slash command and Bash `rm` examples | `$reset-job-profile` | Exact `RESET` confirmation, preserve framework/template files, refusal without confirmation | High: destructive action |
| Salary lookup | Internal to `/apply`, manual CLI | `salary_lookup.py`, `tools/convert_salary_excel.py`, `tools/README_SALARY_TOOL.md`, `salary_data.json` | `/apply` docs mention Claude command | Preserve Python tool and call from `$job-apply` | Missing-data graceful skip, lookup formatting, converter tests | Low |
| Security guards | CI and local checks | `tools/security_guards.py`, `.gitignore`, package manifests | Guard checks `.claude/settings.json` | Extend with Codex compatibility guards while keeping legacy guard during transition | Personal-data ignores, no lifecycle scripts, no active Anthropic requirement | Medium |

## Portal Skills

Existing portal skills already use the open Agent Skills shape and should be
kept under `.agents/skills/`:

| Skill | Commands | Scope |
|---|---|---|
| `jobindex-search` | `search`, `detail` | Jobindex.dk |
| `jobnet-search` | `search`, `detail`, `occupations`, `suggestions` | Jobnet.dk |
| `jobbank-search` | `search`, `detail` | Akademikernes Jobbank |
| `jobdanmark-search` | `search`, `detail`, `categories`, `autocomplete`, `locations` | Jobdanmark.dk |
| `linkedin-search` | `search`, `detail` | LinkedIn public job listings, personal-use-only |
| `freehire-search` | `search`, `detail` | freehire.dev public API, tech-focused |

The migration should preserve their CLIs and tests. Codex workflow skills should
discover these skills dynamically instead of hard-coding a fixed portal list.

## Claude and Anthropic Dependencies

Active Claude-specific assumptions found before migration:

- `README.md` and `SETUP.md` require Claude Code and tell users to run `claude`.
- `SETUP.md` says users need an Anthropic API key or Claude subscription.
- `CLAUDE.md` is the root durable instruction file and candidate profile.
- `.claude/commands/*.md` are the main workflow entry points.
- `.claude/skills/*` contain the core setup/application/scraper/upskill guidance.
- `.claude/settings.json` encodes Claude Code permission allowlists.
- `.claude/agents/gemini-research-expert.md` uses Claude-style agent metadata with `model: sonnet`.
- Workflows refer to Claude tool names: `Read`, `Write`, `Edit`, `Glob`, `Grep`, `WebFetch`, `WebSearch`, `Agent`, and `AskUserQuestion`.
- The reviewer workflow dispatches a Claude `general-purpose` agent.
- `CLAUDE.md` requires generated application documents to mention `Claude Code` by name when referencing agentic coding or AI tooling.

## Migration Principles

- Preserve behavior first; rename only where needed for Codex compatibility.
- Keep `.claude/` and `CLAUDE.md` until Codex replacements pass parity tests.
- Do not remove, simplify, or silently disable workflows.
- Convert tool-name instructions into capability-based Codex instructions.
- Preserve all privacy, confirmation, and no-fabrication rules.
- Keep portal CLIs and LaTeX templates intact.
- Preserve the optional graceful-skip behavior for salary lookup and `pdftotext`.
- Document local environment limitations clearly instead of claiming unavailable checks passed.
