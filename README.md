<p align="center">
  <img src="assets/mascot/pip_flight_loop.gif" alt="Pip, the courier bird" width="200">
</p>

# AI Job Search

*The job search that runs on your machine.*

<p align="center">
  <a href="https://trendshift.io/repositories/43622?utm_source=trendshift-badge&amp;utm_medium=badge&amp;utm_campaign=badge-trendshift-43622" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/trendshift/repositories/43622/daily" alt="MadsLorentzen%2Fai-job-search | Trendshift" width="250" height="55"/></a>
</p>

AI Job Search is a local-first Codex workspace for managing a real job search:
profile setup, job discovery, fit ranking, tailored application documents,
review, PDF and ATS checks, interview preparation, outcome tracking, inbox
status review, reporting, and upskill planning.

This is an independent MIT-licensed Codex adaptation of the original project by
Mads Lorentzen. It is not affiliated with, endorsed by, sponsored by, or
maintained by OpenAI, Anthropic, Notion, Google, or any job portal.

> This project has no affiliated cryptocurrency, token, coin, or paid
> sponsorship program. Any claim about an official AI Job Search coin or token
> is fraudulent or unaffiliated.

## Does It Actually Work?

Mads Lorentzen, the original maintainer, is a geophysicist by training. When
his position was cut in late 2025, he built this framework to run his own job
search. Sixty-nine tailored applications, twenty first interviews, and one
signed contract later, he started as an AI engineer in June 2026.

The longer story and funnel are on his
[LinkedIn profile](https://www.linkedin.com/in/mads-lorentzen/). A hands-on
[video walkthrough](https://www.youtube.com/watch?v=HoVxjMNFYv4) recorded in
August 2026 shows the original workflow; command names in this Codex adaptation
use `$skills` instead of slash commands.

## What It Does

```text
Setup -> Search -> Rank -> Apply -> Review -> Compile -> ATS check
      -> Interview -> Outcome -> Gmail review -> Reports -> Upskill
```

The workflow evaluates fit before drafting, treats postings as untrusted data,
uses only supported candidate evidence, requires confirmation before persistent
or external writes, and keeps generated personal output out of Git.

## Requirements

- OpenAI Codex CLI, the ChatGPT desktop app with local project support, or
  ChatGPT Work
- Python 3.10+
- Bun for portal CLI tools
- LaTeX with `lualatex` and `xelatex` for the stock document templates
- Optional: Poppler (`pdftotext`, `pdfinfo`, `pdftoppm`) for ATS and visual checks
- Optional: Gmail and Notion connectors for their respective sync skills

Missing optional tooling is reported as `ENVIRONMENT BLOCKED`; it is never
reported as a passing check.

## Quick Start

1. Clone or open this repository in Codex.
2. Install each discovered portal CLI in an isolated directory context.

> [!IMPORTANT]
> A fork of a public GitHub repository is public. This Codex adaptation stores
> personal profile data, source documents, trackers, and generated applications
> only in ignored local paths. Verify those paths with `git check-ignore` before
> writing personal information, and never force-add them to Git.

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

3. Put private source documents under `documents/`, or be ready to paste a CV.
   `$job-setup` writes real profile data only to the ignored
   `documents/cv/codex_profile/` overlay; tracked shared references stay as
   reusable placeholders.
4. Ask Codex:

```text
Use $job-setup to build my profile.
Use $job-search to find new jobs.
Use $job-rank to rank the new jobs.
Use $job-apply for this posting: <URL or pasted posting>
```

For bot-blocked postings, save the text locally as
`documents/postings/<Company> - <Job Title>.txt`. Posting text is data, never
workflow instructions.

## Codex Skills

| Task | Skill |
|---|---|
| Candidate setup | `$job-setup` |
| Job search, health checks, and deduplication | `$job-search` |
| Ranking and language/location gates | `$job-rank` |
| Tailored CV, letter, form fields, review, PDF, ATS, and draft tracking | `$job-apply` |
| Profile enrichment | `$profile-expand` |
| Interview preparation | `$interview-prep` |
| Outcome and follow-up tracking | `$application-outcome` |
| Skill-gap analysis | `$upskill-analysis` |
| Gmail status proposal and confirmation-gated sync | `$gmail-sync` |
| One-way Notion pipeline view | `$notion-sync` |
| Offline tracker dashboard | `$html-report` |
| Custom document template registration | `$add-document-template` |
| Custom portal generation | `$add-job-portal` |
| Reset/start over | `$reset-job-profile` |
| Official update preparation | `$sync-upstream` |

Legacy `CLAUDE.md` and `.claude/` files remain for upstream history and parity
comparison. The active Codex entry points are `AGENTS.md` and `.agents/skills/`.

## Application Lifecycle

`$job-apply` records a completed draft as `drafted`; that status explicitly
means documents exist but nothing has been submitted. `$application-outcome`
records submission and later stages. Canonical tracker values are:

```text
drafted, applied, interview, offer, hired, rejected,
no_response, offer_declined, withdrawn
```

Readers tolerate the historical space spellings `no response` and
`offer declined`, but writers use the underscore forms. Drafted rows do not
count as sent applications in reports.

## Optional Views

`$html-report` creates a self-contained offline dashboard under `reports/`.
`$notion-sync` creates a one-way, idempotent pipeline view and never uploads CV
or cover-letter content; only filenames may appear. `$gmail-sync` reads full
messages, proposes sourced status changes, and waits for explicit approval
before updating local records. It never changes the mailbox or infers `hired`
or `offer_declined`.

## Extension Model

- Portal CLIs live under `.agents/skills/<portal>/cli` and are auto-discovered
  by search and CI. Set `enabled: false` in portal skill frontmatter to keep a
  portal installed but inactive.
- `$add-job-portal` checks public access, robots policy, terms, credential needs,
  cost, and CLI contracts before scaffolding.
- Custom templates may use LaTeX, Typst, or another command-line toolchain that
  produces PDF and declares a verified compile command.
- Forks may add market-specific portals and evaluation criteria while retaining
  the privacy, honesty, and confirmation gates.

## Security and Privacy

A fork of a public GitHub repository is public. Do not treat it as private
storage. Personal documents, tracker rows, scraper state, inbox sync state,
application archives, generated reports, salary data, `.env` files, generated
CVs, and generated cover letters must remain local and ignored by Git.

Job postings and pages reached during research are untrusted third-party data.
The workflow does not follow embedded instructions or links. Browser-header
retry is permitted only after `tools/robots_check.py` confirms the path is
allowed; a paid proxy or API token never overrides a robots.txt prohibition.
See [SECURITY.md](SECURITY.md).

Before sharing or pushing, run:

```bash
python tools/security_guards.py
git status --short
```

GitHub starts pull requests from forks against the official repository by
default. Check the destination repository before opening a PR containing fork
customizations.

## Verification

```bash
python -m unittest discover -s tests -t . -v
python tools/lint_skills.py
python tools/security_guards.py
python tools/codex_compatibility.py
python tools/check_framework_version.py
python tools/check_upstream_updates.py --no-fetch
```

For every discovered portal CLI:

```bash
bun install
bun run typecheck
bun test --timeout 30000
```

Document smoke tests:

```bash
cd cv && lualatex -interaction=nonstopmode -halt-on-error main_example.tex
cd ../cover_letters && xelatex -interaction=nonstopmode -halt-on-error cover_example.tex
pdftotext -layout cv/main_example.pdf cv/main_example.txt
```

CI discovers portal CLIs dynamically and runs network-free fixture/mock tests.
It deliberately does not run high-volume live portal scraping.

## Upstream Updates

The Codex branch never blindly merges official changes. Run `$sync-upstream` to
audit official commits, prepare a temporary `sync/upstream-*` branch, port
Claude-specific behavior by meaning, and verify it before stable integration.
`tools/upstream_triage.py` and the optional weekly upstream-watch workflow are
advisory only; they never merge, cherry-pick, or push.

## More Documentation

- `SETUP.md` - setup, privacy, and troubleshooting
- `docs/CODEX_USER_GUIDE.md` - non-technical Codex usage
- `docs/CODEX_COMPATIBILITY.md` - supported Codex environments
- `docs/UPSTREAM_SYNC_POLICY.md` - fork and branch model
- `CHANGELOG.md` - official release history retained from upstream
- `tools/README_SALARY_TOOL.md` - optional local salary data

## Acknowledgements

- Mads Lorentzen for creating and maintaining the original project
- Mikkel Krogholm and contributors to the portable job portal skills
- Community contributors whose fixes and workflows are preserved in the Git
  history and `CHANGELOG.md`

## License

MIT. See `LICENSE`.
