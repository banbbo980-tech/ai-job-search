# AI Job Search

<p align="center">
  <a href="https://trendshift.io/repositories/43622?utm_source=trendshift-badge&amp;utm_medium=badge&amp;utm_campaign=badge-trendshift-43622" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/trendshift/repositories/43622/daily" alt="MadsLorentzen%2Fai-job-search | Trendshift" width="250" height="55"/></a>
</p>

AI Job Search is a local-first Codex workspace for managing a real job search:
profile setup, job discovery, fit ranking, tailored LaTeX CVs and cover letters,
review, PDF/ATS checks, interview preparation, outcome tracking, and upskill
planning.

This is an independent MIT-licensed project migrated from the original
Claude Code-oriented workflow by Mads Lorentzen. It is not affiliated with,
endorsed by, sponsored by, or maintained by OpenAI, Anthropic, or any job portal.

> This project has **no affiliated cryptocurrency, token, coin, or paid
> sponsorship program**. Any claim about an official AI Job Search coin or token
> is fraudulent or unaffiliated.

## What It Does

The workflow keeps your private career material on your machine and helps you
move through a full application loop:

```text
Setup -> Search -> Rank -> Apply -> Review -> Compile -> ATS check
      -> Interview prep -> Outcome tracking -> Upskill analysis
```

The project preserves the original behavior: fit is evaluated before drafting,
applications are based only on supported candidate evidence, PDF layout is
checked after LaTeX compilation, ATS text extraction is verified when available,
and destructive resets require explicit confirmation.

## Requirements

- OpenAI Codex CLI, ChatGPT desktop app with local project support, or ChatGPT Work
- Python 3.10+
- Bun for the job-portal CLI tools
- LaTeX with `lualatex` and `xelatex`
- Optional: `pdftotext` from Poppler for ATS text-layer checks

If Bun, LaTeX, or `pdftotext` are not installed locally, the related workflow
step reports a clear environment block instead of pretending verification passed.

## Quick Start

1. Clone or open this repository in Codex.
2. Install portal CLI dependencies:

```bash
for tool in freehire-search jobbank-search jobdanmark-search jobindex-search jobnet-search linkedin-search; do
  cd .agents/skills/$tool/cli
  bun install
  cd ../../../..
done
```

PowerShell:

```powershell
$tools = @("freehire-search", "jobbank-search", "jobdanmark-search", "jobindex-search", "jobnet-search", "linkedin-search")
foreach ($tool in $tools) {
  Set-Location ".agents/skills/$tool/cli"
  bun install
  Set-Location "..\..\..\.."
}
```

3. Add your career documents under `documents/` or be ready to paste a CV.
4. Ask Codex:

```text
Use $job-setup to build my profile.
```

5. Search and apply:

```text
Use $job-search to find new jobs.
Use $job-rank to rank the scraped jobs.
Use $job-apply for this job posting: <URL or pasted posting>
```

## Codex Skills

| Task | Skill |
|---|---|
| Candidate setup | `$job-setup` |
| Job search and deduplication | `$job-search` |
| Ranking scraped jobs | `$job-rank` |
| Tailored application package | `$job-apply` |
| Profile enrichment | `$profile-expand` |
| Interview preparation | `$interview-prep` |
| Outcome tracking | `$application-outcome` |
| Skill-gap analysis | `$upskill-analysis` |
| Custom LaTeX template registration | `$add-document-template` |
| Custom portal generation | `$add-job-portal` |
| Reset/start over | `$reset-job-profile` |

Natural language works too. For example: "Find remote data jobs near Berlin" can
trigger the job-search workflow when Codex has the project skills available.

## Old Workflow Mapping

| Old Claude workflow | New Codex skill |
|---|---|
| `/setup` | `$job-setup` |
| `/scrape` | `$job-search` |
| `/rank` | `$job-rank` |
| `/apply <url>` | `$job-apply` |
| `/expand` | `$profile-expand` |
| `/interview` | `$interview-prep` |
| `/outcome` | `$application-outcome` |
| `/upskill` | `$upskill-analysis` |
| `/add-template` | `$add-document-template` |
| `/add-portal` | `$add-job-portal` |
| `/reset` | `$reset-job-profile` |

## File Structure

```text
AGENTS.md                         Codex project guidance
.agents/skills/                   Codex workflow skills and portal skills
.agents/skills/job-application-core/references/
                                  Shared profile, evaluation, writing, template, and search rules
.claude/                          Legacy files retained during parity migration
cv/                               LaTeX CV templates and generated CVs
cover_letters/                    LaTeX cover-letter templates and generated letters
documents/                        Local private career documents and application archives
job_scraper/                      Seen-job state
templates/                        Custom registered LaTeX templates
upskill/                          Generated learning reports
tools/                            Lint, security, salary, and compatibility checks
docs/                             Codex migration and user documentation
```

## Verification

Run the checks available in your environment:

```bash
python -m unittest discover -s tests -t . -v
python tools/lint_skills.py
python tools/security_guards.py
python tools/codex_compatibility.py
```

With Bun installed, run each portal CLI's checks:

```bash
cd .agents/skills/<portal-skill>/cli
bun install
bun run typecheck
bun test --timeout 30000
```

With LaTeX installed:

```bash
cd cv && lualatex -interaction=nonstopmode -halt-on-error main_example.tex
cd ../cover_letters && xelatex -interaction=nonstopmode -halt-on-error cover_example.tex
```

With Poppler installed:

```bash
pdftotext -layout cv/main_example.pdf cv/main_example.txt
```

## Privacy

Personal documents, generated applications, tracker files, salary data, scraper
state, and upskill reports are ignored by Git. Review `git status` before
sharing or committing from a personalized fork.

## More Documentation

- `SETUP.md` - setup and troubleshooting
- `docs/CODEX_USER_GUIDE.md` - non-technical user guide
- `docs/CODEX_COMPATIBILITY.md` - environment compatibility notes
- `docs/CODEX_TEST_REPORT.md` - latest migration verification report
- `tools/README_SALARY_TOOL.md` - optional salary data setup

## License

MIT. See `LICENSE`.
