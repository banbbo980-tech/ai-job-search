# Setup Guide

This guide gets AI Job Search running in Codex CLI, the ChatGPT desktop app with
a local project, or ChatGPT Work.

## 1. Install Prerequisites

### Codex

Use one of these surfaces:

- **Codex CLI:** open the repository in your terminal and run Codex there.
- **ChatGPT desktop app:** open this folder as a local project.
- **ChatGPT Work:** attach or connect the repository according to your workspace
  policy.

Codex reads the root `AGENTS.md` and the project skills under `.agents/skills/`.

### Python

Python 3.10+ is required for salary lookup and tests.

```bash
python --version
```

### Bun

The portal search tools are TypeScript CLIs that run with Bun.

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -c "irm https://bun.sh/install.ps1 | iex"
```

macOS/Linux:

```bash
curl -fsSL https://bun.sh/install | bash
```

Install portal dependencies from the repository root:

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

### LaTeX

Install a LaTeX distribution that includes `lualatex` and `xelatex`.

- Windows: MiKTeX
- macOS: MacTeX or TinyTeX
- Linux: TeX Live

The stock CV compiles with `lualatex`. The stock cover letter compiles with
`xelatex` because `cover.cls` uses custom fonts.

Smoke tests:

```bash
cd cv && lualatex -interaction=nonstopmode -halt-on-error main_example.tex
cd ../cover_letters && xelatex -interaction=nonstopmode -halt-on-error cover_example.tex
```

### Optional: pdftotext

`$job-apply` uses Poppler's `pdftotext` for ATS verification.

- macOS: `brew install poppler`
- Debian/Ubuntu: `sudo apt install poppler-utils`
- Windows: install Poppler through your preferred package manager

Check:

```bash
pdftotext -v
```

If unavailable, `$job-apply` reports reduced ATS verification.

## 2. Add Career Documents Safely

Use `documents/` for private local inputs:

- `documents/cv/`
- `documents/linkedin/`
- `documents/diplomas/`
- `documents/references/`
- `documents/applications/`

These contents are ignored by Git. Keep real personal data out of README files,
tests, examples, and reusable templates.

## 3. Run Candidate Setup

Ask Codex:

```text
Use $job-setup to build my profile.
```

Setup offers three paths:

- Read the `documents/` folder.
- Import a single pasted or attached CV.
- Walk through interview-style onboarding.

To update only search configuration:

```text
Use $job-setup --section search.
```

## 4. Search, Rank, and Apply

```text
Use $job-search to find new jobs.
Use $job-rank to rank the scraped jobs.
Use $job-apply for this job posting: <URL or pasted job description>
```

When a URL cannot be fetched, paste the full job description. The workflow will
not fabricate posting details from search snippets.

## 5. Track Interviews and Outcomes

```text
Use $interview-prep for my interview at <company>.
Use $application-outcome to record what happened with <company>.
Use $upskill-analysis to identify what I should learn next.
```

## 6. Optional Salary Data

If you have salary data, create `salary_data.json` or convert an Excel file:

```bash
python tools/convert_salary_excel.py path/to/salary-data.xlsx --source "My Salary Data 2026"
```

If no salary data is configured, `$job-apply` skips salary lookup gracefully.

## 7. Verify the Project

```bash
python -m unittest discover -s tests -t . -v
python tools/lint_skills.py
python tools/security_guards.py
python tools/codex_compatibility.py
```

Run Bun and LaTeX checks when those tools are installed. Environment-blocked
checks are not migration success; report them as blocked.

## Troubleshooting

### Bun is missing

Portal CLIs cannot run. Install Bun, restart the terminal/app if needed, and run
`bun --version`.

### LaTeX is missing

Application drafting can still create `.tex` files, but PDF compile/layout
verification is blocked until `lualatex` and `xelatex` are installed.

### pdftotext is missing

ATS text-layer verification runs in reduced mode. Install Poppler for the full
check.

### Salary data is missing

This is expected unless you configured salary benchmarking. `$job-apply` skips
the optional benchmark.

### A portal blocks access

Some portals block automated requests or restrict scraping. The workflow reports
that honestly and lets you paste the full posting.
