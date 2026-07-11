# Codex User Guide

This guide is for non-technical users running AI Job Search with Codex or
ChatGPT Work.

## The Basic Loop

1. Add career documents to `documents/`.
2. Run setup:

```text
Use $job-setup to build my profile.
```

3. Search for jobs:

```text
Use $job-search to find new jobs.
```

4. Rank the results:

```text
Use $job-rank to rank the scraped jobs.
```

5. Apply to a role:

```text
Use $job-apply for this job posting: <paste URL or full job description>
```

6. After submitting:

```text
Use $application-outcome to record the application.
```

7. Before interviews:

```text
Use $interview-prep for my interview at <company>.
```

8. For learning priorities:

```text
Use $upskill-analysis to identify my skill gaps.
```

9. To check for official project updates:

```text
Use $sync-upstream to check the official repository for updates.
```

## What to Put in documents/

- `documents/cv/`: your most complete CV or resume.
- `documents/linkedin/`: a LinkedIn profile export or PDF.
- `documents/diplomas/`: diplomas, transcripts, certificates.
- `documents/references/`: recommendation or reference letters.
- `documents/applications/`: past application folders.

These folders are ignored by Git so your private files stay local.

## How Applications Are Made

`$job-apply` always starts with fit evaluation. It should tell you:

- Why the job matches.
- What is missing.
- Whether any deal-breaker appears.
- Whether the deadline is urgent.
- Whether it recommends applying.

It then asks whether to proceed. If you say yes, it creates a tailored CV and
cover letter, has a separate reviewer pass check them, revises valid findings,
compiles PDFs when LaTeX is available, checks layout, and runs ATS verification
when `pdftotext` is available.

The workflow must not invent experience just to match keywords.

## Old to New Command Table

| Previously | Now |
|---|---|
| `/setup` | `$job-setup` |
| `/scrape` | `$job-search` |
| `/rank` | `$job-rank` |
| `/apply` | `$job-apply` |
| `/expand` | `$profile-expand` |
| `/interview` | `$interview-prep` |
| `/outcome` | `$application-outcome` |
| `/upskill` | `$upskill-analysis` |
| `/add-template` | `$add-document-template` |
| `/add-portal` | `$add-job-portal` |
| `/reset` | `$reset-job-profile` |

## Privacy Checklist

Before sharing the repository:

```bash
git status --short
```

Do not commit:

- Real CVs or LinkedIn exports.
- Generated tailored applications.
- `job_search_tracker.csv`.
- `salary_data.json`.
- Scraper state.
- Upskill reports.

## GitHub And Branches

`upstream` means the official project by Mads Lorentzen. It is the source this
Codex version watches for future changes.

`origin` means your GitHub fork after it is created. It is the place your
Codex-native branch can be pushed.

Use `codex-migration` for normal Codex work. Official updates should first go
into a temporary branch named like `sync/upstream-2026-07-11-c134eef`, then be
tested before they are merged back.

Check for updates with:

```bash
python tools/check_upstream_updates.py
```

Do not blindly merge official updates into `codex-migration`, because the
official project can contain Claude-specific commands or instructions that must
be converted into Codex skills.

## Troubleshooting

If job search does not run, check Bun:

```bash
bun --version
```

If PDF verification is blocked, check LaTeX:

```bash
lualatex --version
xelatex --version
```

If ATS verification is reduced, check Poppler:

```bash
pdftotext -v
```

If a portal blocks access, paste the complete job posting into chat and run
`$job-apply` with that text.
