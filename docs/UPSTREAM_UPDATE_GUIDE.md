# Upstream Update Guide

Use this guide when you want to check whether the official AI Job Search project
has changed.

## Check For Updates

From `codex-migration`:

```bash
git status --short
python tools/check_upstream_updates.py
```

If the checker says the project is up to date, no action is needed.

If it reports updates, use:

```text
Use $sync-upstream to prepare the official update.
```

Codex will create a temporary sync branch, convert the official changes, run
tests, and show a report before anything is merged into the stable Codex branch.

## Why Not Merge Directly?

The official project may contain Claude Code commands, Claude-specific tool
names, or Anthropic setup instructions. This fork must stay usable in OpenAI
Codex and ChatGPT Work. Direct merges can accidentally reintroduce those
requirements or remove Codex behavior.

## Recovery On Another Computer

After the GitHub fork is configured and pushed:

```bash
git clone <your-fork-url> "ai job search"
cd "ai job search"
git remote add upstream https://github.com/MadsLorentzen/ai-job-search.git
git fetch upstream
git switch codex-migration
python -m unittest discover -s tests -t . -v
python tools/security_guards.py
python tools/codex_compatibility.py
```

If `origin` is missing, add it with the user's fork URL. If `upstream` is
missing, add the official URL shown above.

## Files With Rules

- `AGENTS.md`: active Codex project rules.
- `.agents/skills/*/SKILL.md`: active Codex workflows.
- `.agents/skills/job-application-core/references/`: shared profile, writing,
  evaluation, template, and query references.
- `docs/UPSTREAM_SYNC_POLICY.md`: branch model and upstream update process.

## Files With Personal Information

The following should stay local and are ignored by Git:

- `documents/cv/`
- `documents/linkedin/`
- `documents/diplomas/`
- `documents/references/`
- `documents/applications/`
- `cv/main_*.tex` except `cv/main_example.tex`
- `cover_letters/cover_*.tex` except `cover_letters/cover_example.tex`
- `job_search_tracker.csv`
- `salary_data.json`
- `job_scraper/seen_jobs.json`
- `upskill/*.md`

## Files Safe To Push

Project code, tests, docs, example templates, sanitized fixtures, and Codex
skills are intended to be pushed. Run `python tools/security_guards.py` before
any push.

## Blocked Production Tools

This machine currently needs these tools before full production verification:

| Tool | Needed for | Verify with |
|---|---|---|
| Bun | Official portal CLI install, typecheck, and test workflow. | `bun --version` |
| MiKTeX or TeX Live | `lualatex` CV compile and `xelatex` cover-letter compile. | `lualatex --version`, `xelatex --version` |
| Poppler | `pdftotext` ATS extraction and reading-order checks. | `pdftotext -v` |
| GitHub CLI | Fork creation, auth inspection, and safe push setup. | `gh --version`, `gh auth status` |

Do not install these globally or change system-wide settings without user
approval.
