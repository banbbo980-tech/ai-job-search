# Setup Guide

This guide configures AI Job Search for Codex CLI, the ChatGPT desktop app with
a local project, or ChatGPT Work.

## 1. Install Prerequisites

### Codex

Open the repository as the working directory. Codex reads `AGENTS.md` and the
skills under `.agents/skills/`. The legacy `.claude/` tree is retained for
upstream parity and is not the active runtime.

### Python

Python 3.10+ is required for tests and local tools.

```bash
python --version
```

### Bun

Portal tools are TypeScript CLIs built for Bun. Install Bun for the current
user using the official Bun instructions or your normal package manager. Do not
install global software or change system-wide configuration from an automated
workflow without explicit approval.

Verify:

```bash
bun --version
```

Install all discovered portal dependencies with failure isolated per portal.

PowerShell:

```powershell
Get-ChildItem .agents/skills -Directory | ForEach-Object {
  $cli = Join-Path $_.FullName "cli"
  if (Test-Path (Join-Path $cli "package.json")) {
    Push-Location $cli
    try { bun install } finally { Pop-Location }
  }
}
```

Bash:

```bash
find .agents/skills -mindepth 3 -maxdepth 3 -path '*/cli/package.json' -print0 |
while IFS= read -r -d '' manifest; do
  (cd "$(dirname "$manifest")" && bun install)
done
```

### LaTeX

The stock CV uses `lualatex`; the stock cover letter uses `xelatex` because
`cover.cls` uses `fontspec`.

- Windows: MiKTeX
- macOS: MacTeX, BasicTeX, or TinyTeX
- Linux: TeX Live

Minimal TeX installations need these packages:

```bash
tlmgr install \
  moderncv fontawesome5 fontawesome6 academicons import luatexbase pgf \
  titlesec textpos xltxtra xunicode cite realscripts needspace
```

For BasicTeX or MacTeX, ensure `/Library/TeX/texbin` is on `PATH` before
running `tlmgr`.

For a user-level TinyTeX install on macOS:

```bash
curl -fsSL https://yihui.org/tinytex/install-bin-unix.sh -o /tmp/tinytex-install-bin-unix.sh
sh /tmp/tinytex-install-bin-unix.sh /tmp --no-path
export PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"
```

For Basic MiKTeX on Windows, preinstall the required packages or configure
MiKTeX package auto-installation for the current user so a non-interactive
compile cannot stall on a GUI prompt. A locked-down production verification
may use `--disable-installer` after packages are present.

PowerShell smoke tests:

```powershell
Push-Location cv
lualatex --disable-installer --halt-on-error --interaction=nonstopmode main_example.tex
Pop-Location
Push-Location cover_letters
xelatex --disable-installer --halt-on-error --interaction=nonstopmode cover_example.tex
Pop-Location
```

### Poppler

Poppler provides `pdftotext`, `pdfinfo`, and `pdftoppm` for ATS, page-count,
and rendering checks.

```bash
pdftotext -v
pdfinfo -v
pdftoppm -v
```

If Bun, LaTeX, or Poppler is unavailable, report the related check as
`ENVIRONMENT BLOCKED` and preserve CI coverage.

## 2. Add Private Career Data

> [!IMPORTANT]
> A fork of a public GitHub repository is public. This Codex adaptation keeps
> personal data, source documents, trackers, and generated applications in
> ignored local paths. Never force-add those files. Use a separate private
> repository only if personal material must be stored remotely.

Use these local paths:

- `documents/cv/`
- `documents/linkedin/`
- `documents/diplomas/`
- `documents/references/`
- `documents/postings/`
- `documents/applications/`
- `documents/cv/codex_profile/` for the generated private profile overlay

Before writing personal data, run `git check-ignore -v <path>` and
`git ls-files --error-unmatch <path>`. Stop if the target is tracked. A public
GitHub fork cannot be treated as private storage; use ignored local files or a
separate private repository for personalized tracked content.

## 3. Build the Candidate Profile

```text
Use $job-setup to build my profile.
```

Setup can read the documents folder, import one CV, or interview the user.
It records languages with honest proficiency levels for the Language Gate and
records the preferred CV language separately. Danish demonstration portals
ship disabled and are enabled only for users who want the Danish market.
Tracked files under `.agents/skills/job-application-core/references/` remain
framework templates; setup never writes personal facts there.

To refresh search settings only:

```text
Use $job-setup --section search.
```

## 4. Search, Rank, and Apply

```text
Use $job-search to find new jobs.
Use $job-rank to rank the new jobs.
Use $job-apply for this posting: <URL or pasted posting>
```

Portal skills are auto-discovered. A portal with `enabled: false` remains
installed but is skipped. Use `$job-search health` for bounded parser health
checks without a high-volume live search.

When a URL cannot be fetched, save or paste the complete posting. Do not draft
from a title or search snippet. The workflow checks robots.txt before any
browser-header retry and never treats a paid fetcher as permission to bypass a
prohibition.

`$job-apply` evaluates eligibility and fit before drafting. After confirmation
it creates role-specific document names, optionally creates application-form
answers, runs an independent review, compiles and visually checks PDFs, verifies
ATS extraction, records a `drafted` tracker row, and archives the full posting.
Nothing is submitted automatically.

## 5. Track the Lifecycle

```text
Use $interview-prep for my interview at <company>.
Use $application-outcome to record what happened with <company>.
Use $upskill-analysis to identify what I should learn next.
```

`$application-outcome` owns the canonical tracker vocabulary and can draft up
to two follow-up messages for quiet applications. It never sends them.

## 6. Optional Integrations

### Gmail

Connect a Gmail connector in the current Codex or ChatGPT environment, then:

```text
Use $gmail-sync to review application-status emails.
```

The skill reads full messages, proposes sourced changes, and pauses for explicit
approval before writing local tracker/archive state. It never modifies Gmail.

### Notion

Install and authenticate the Notion connector supported by your Codex or
ChatGPT environment, then:

```text
Use $notion-sync to refresh my pipeline view.
```

The repository remains the source of truth. The sync is one-way, idempotent,
and uploads no CV or cover-letter contents.

### Offline HTML Dashboard

```text
Use $html-report to generate my application dashboard.
```

The self-contained report is written under `reports/`, which is ignored by Git.

## 7. Optional Salary Data

Create local `salary_data.json`, or convert a workbook:

```bash
python tools/convert_salary_excel.py path/to/salary-data.xlsx --source "My Salary Data 2026"
python salary_lookup.py --validate
```

Salary data remains local. `$job-apply` skips lookup gracefully when it is not
configured.

## 8. Verify the Project

```bash
python -m unittest discover -s tests -t . -v
python tools/lint_skills.py
python tools/security_guards.py
python tools/codex_compatibility.py
python tools/check_framework_version.py
python tools/check_upstream_updates.py --no-fetch
```

For every `.agents/skills/*/cli/package.json`, run:

```bash
bun install
bun run typecheck
bun test --timeout 30000
```

## 9. Pull Official Updates Safely

Keep the official repository configured separately:

```bash
git remote add upstream https://github.com/MadsLorentzen/ai-job-search.git
git fetch upstream --prune --tags
python tools/check_upstream_updates.py --no-fetch
python tools/upstream_triage.py --remote upstream --branch master
```

Use `$sync-upstream` to prepare a temporary branch. Never merge official
updates directly into `codex-migration`, and never push to `upstream`.
`upstream-watch.yml` is advisory only and, when enabled on a fork, updates one
issue in that fork. It does not merge or push.

## Troubleshooting

- `bun` missing: portal CLI checks are environment-blocked; use a permitted web
  fallback or install Bun for the current user.
- LaTeX missing: source drafts can be created, but PDF verification is blocked.
- `pdftotext` missing: ATS verification is reduced and must be reported that way.
- Portal 429/5xx: shipped CLIs use bounded retry/backoff and 15-second request
  timeouts; do not increase volume to compensate.
- Connector unavailable: Gmail and Notion skills exit cleanly without changing
  local state.
