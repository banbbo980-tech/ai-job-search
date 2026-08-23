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

## Production Tool Check

Check these tools on the current machine before verification. Availability can
change; never describe a check as passed merely because the tool is listed here.

| Tool | Needed for | Verify with |
|---|---|---|
| Bun | Official portal CLI install, typecheck, and test workflow. | `bun --version` |
| MiKTeX or TeX Live | `lualatex` CV compile and `xelatex` cover-letter compile. | `lualatex --version`, `xelatex --version` |
| Poppler | `pdftotext` ATS extraction and reading-order checks. | `pdftotext -v` |
| GitHub CLI | Fork creation, auth inspection, and safe push setup. | `gh --version`, `gh auth status` |

Do not install these globally or change system-wide settings without user
approval.

## Complete Audited Process

Use the process below for every official update. Commit SHAs, not GitHub's
ahead/behind banner or dates, are the source of truth.

### 1. Preflight

Start on `codex-migration`:

```powershell
git status --short
git branch --show-current
git rev-parse HEAD
git remote -v
git ls-files
```

Stop if the worktree is dirty, `origin` is not the user's fork, `upstream` is
not `https://github.com/MadsLorentzen/ai-job-search.git`, or personal/generated
files are tracked. Verify `AGENTS.md`, `.agents/skills/`, `CLAUDE.md`, `.claude/`,
and `docs/upstream-state.json` exist.

### 2. Fetch And Identify Exact Official Changes

```powershell
git fetch origin
git fetch upstream --tags
python tools/check_upstream_updates.py --no-fetch
python tools/upstream_triage.py --remote upstream --branch master
git log --reverse --format="%H %s" <recorded-sha>..upstream/master
git diff --name-status <recorded-sha>..upstream/master
```

Audit every commit, changed/deleted file, release tag, security change, portal
change, template change, test change, and Claude-specific file before editing.

### 3. Create A Temporary Branch And Preserve History

```powershell
git switch -c sync/upstream-YYYY-MM-DD-<short-sha> codex-migration
git merge --no-ff --no-commit upstream/master
```

Resolve conflicts on this temporary branch only. Commit the import as a merge so
the complete official commit graph remains visible. Never import directly on
`codex-migration`.

### 4. Convert Official Behavior For Codex

Conflict priorities are privacy and confirmation gates first, active Codex
behavior second, and official functionality/history third. Keep legacy Claude
files for parity, but do not restore Claude or Anthropic as a runtime.

| Official source | Active Codex destination |
|---|---|
| `CLAUDE.md` project behavior | `AGENTS.md` and affected Codex skills |
| `.claude/commands/apply.md` | `.agents/skills/job-apply/SKILL.md` |
| `.claude/commands/interview.md` | `.agents/skills/interview-prep/SKILL.md` |
| `.claude/commands/outcome.md` | `.agents/skills/application-outcome/SKILL.md` |
| `.claude/commands/setup.md` | `.agents/skills/job-setup/SKILL.md` |
| `.claude/commands/rank.md` | `.agents/skills/job-rank/SKILL.md` |
| `.claude/commands/reset.md` | `.agents/skills/reset-job-profile/SKILL.md` |
| Gmail, Notion, HTML commands | Matching Codex skill |
| Job-scraper methodology | `$job-search` and the search-query reference |
| Evaluation/template methodology | `job-application-core/references/` |
| Claude reviewer/tool names | Codex subagent plus fallback/capability wording |
| Portal TypeScript/Bun code | Existing `.agents/skills/<portal>/cli/` |

Convert by meaning and user-visible behavior, never by blind word replacement.
Add Codex parity tests because official tests may exercise only `.claude/`.

### 5. Run Full Verification

```powershell
python -m unittest discover -s tests -t . -v
python tools/lint_skills.py
python tools/security_guards.py
python tools/codex_compatibility.py
python tools/check_framework_version.py
python tools/check_upstream_updates.py --no-fetch
git diff --check
```

Run every discovered portal CLI in its own folder:

```powershell
Get-ChildItem .agents/skills -Directory | ForEach-Object {
  $cli = Join-Path $_.FullName "cli"
  if (Test-Path (Join-Path $cli "package.json")) {
    Push-Location $cli
    try {
      bun install
      bun run typecheck
      bun test --timeout 30000
    } finally { Pop-Location }
  }
}
```

Compile each example twice, then verify page count, every rendered page, and ATS
text extraction:

```powershell
Push-Location cv
lualatex --disable-installer --halt-on-error --interaction=nonstopmode main_example.tex
lualatex --disable-installer --halt-on-error --interaction=nonstopmode main_example.tex
Pop-Location
Push-Location cover_letters
xelatex --disable-installer --halt-on-error --interaction=nonstopmode cover_example.tex
xelatex --disable-installer --halt-on-error --interaction=nonstopmode cover_example.tex
Pop-Location
pdftotext -layout -enc UTF-8 cv/main_example.pdf "$env:TEMP\ai-job-cv-ats.txt"
pdftotext -layout -enc UTF-8 cover_letters/cover_example.pdf "$env:TEMP\ai-job-cover-ats.txt"
```

If Bun, LaTeX, or Poppler is unavailable, report the related check as environment
blocked. Use fictional data only. Delete temporary extracted/rendered files.

Privacy checks must include ignored profile, application, posting, cache,
tracker, report, and generated document probes:

```powershell
python tools/security_guards.py
git status --short
git check-ignore -v documents/cv/codex_profile/01-candidate-profile.md
git check-ignore -v documents/applications/example/job_posting.md
git check-ignore -v documents/postings/example.txt
git check-ignore -v company_research/example.json
git check-ignore -v job_search_tracker.csv
git check-ignore -v reports/example.html
```

### 6. Report And Commit The Temporary Branch

Create `docs/upstream-updates/YYYY-MM-DD_<short-sha>.md` containing exact commits,
files changed, conflicts, the Claude-to-Codex parity table, exact test results,
security/privacy results, environment blocks, remaining risks, branch name, and
final SHA.

Use logical commits: official-history import, Codex conversion/tests, then
verification documentation. Do not update `docs/upstream-state.json` to the new
official SHA until conversion passes and the user approves stable integration.

### 7. Approval, Stable Merge, And Push

Stop and ask before changing `codex-migration`. After approval, fetch both
remotes again, verify all expected SHAs, and use only:

```powershell
git switch codex-migration
git merge --ff-only sync/upstream-YYYY-MM-DD-<short-sha>
```

If fast-forward fails, stop. Do not rebase, reset, force, or choose another merge
method. Update the state/report as part of the approved integration and rerun the
required checks.

Immediately before pushing:

```powershell
python tools/security_guards.py
git status --short
git push origin codex-migration
```

Never push the temporary branch unless explicitly requested. Never push to
`upstream`, force-push, modify `master`, or upload personal/generated files.

### 8. Verify After Push

```powershell
git fetch origin
git rev-parse codex-migration
git rev-parse origin/codex-migration
git merge-base --is-ancestor upstream/master codex-migration
```

Verify GitHub shows the expected stable commit, official ancestry, active Codex
skills, green CI, and no personal files. Keep the temporary branch until final
production verification is complete.
