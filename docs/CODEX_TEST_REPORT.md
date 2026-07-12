# Codex Test Report

Latest local verification for the Codex production-verification branch.

Branch: `fix/production-verification-2026-07-12`
Base stable commit: `971d0b9f3b9f3447ae472d5466c0c7bdfed2d59d`
Recorded official upstream commit: `8bee3ddb9731b715908dbde288f457e541b3d7dc`
Verification date: 2026-07-12

## Installed Tooling

| Tool | Version | Source | Install scope | Executable |
|---|---:|---|---|---|
| Bun | `1.3.14+0d9b296af` | Official Bun PowerShell installer from `https://bun.com/docs/installation` | Current user | `%USERPROFILE%\.bun\bin\bun.exe` |
| MiKTeX | `25.12` | Official MiKTeX Basic Installer `basic-miktex-25.12-x64.exe` from `https://miktex.org/download` | Private current-user install | `%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64\lualatex.exe`; `...\xelatex.exe` |
| Poppler | `26.02.0` | Project-documented Poppler Windows release `v26.02.0-0` from `https://github.com/oschwartz10612/poppler-windows/releases` | Portable current-user install | `%LOCALAPPDATA%\Programs\poppler-26.02.0-0\Library\bin\pdftotext.exe` |

MiKTeX package database refresh was attempted and failed with
`Couldn't resolve host name`. The compilers still worked. The cover-letter smoke
test required the MiKTeX package `titlesec`, which was installed with
`miktex packages require titlesec`.

## Automated Checks

| Command | Result |
|---|---|
| `python -m unittest discover -s tests -t . -v` | Passed: 88 tests in 67.053s |
| `python tools/lint_skills.py` | Passed: `lint_skills: OK (22 skills, 9 commands, settings.json)` |
| `python tools/security_guards.py` | Passed: `security_guards: OK (permissions allowlist, gitignore rules, package manifests)` |
| `python tools/codex_compatibility.py` | Passed: `codex_compatibility: OK (13 workflow skills, 8 shared references, AGENTS.md)` |
| `python tools/check_upstream_updates.py --no-fetch` | Safe stop: working tree is intentionally dirty with uncommitted production-verification fixes |

`check_upstream_updates.py --no-fetch` should be rerun after the fix branch is
committed or otherwise made clean. The recorded upstream state still identifies
`8bee3dd` as the integrated official commit.

## Bun Portal Checks

Each portal ran `bun install --no-progress`, `bun run typecheck`, and
`bun run test` with Bun `1.3.14`.

| Portal skill | Install | Typecheck | Tests |
|---|---|---|---|
| `jobbank-search` | Passed, no changes | Passed | Passed: 1 test, 1 expect |
| `jobdanmark-search` | Passed, no changes | Passed | Passed: 1 test, 9 expects |
| `jobindex-search` | Passed, no changes | Passed | Passed: 6 tests, 6 expects |
| `jobnet-search` | Passed, no changes | Passed | Passed: 1 test, 1 expect |
| `linkedin-search` | Passed, no changes | Passed | Passed: 17 tests, 26 expects |
| `freehire-search` | Passed, no changes | Passed | Passed: 26 tests, 56 expects |

The `bun.lock` files and `node_modules/` directories created by local Bun
installs are ignored by Git.

## PDF And ATS Checks

| Check | Result |
|---|---|
| Example CV compile | Passed with `lualatex`; output `main_example.pdf` is 2 pages |
| Example CV visual inspection | Passed after fixing clipped `moderncv` achievement bullets |
| Example cover-letter compile | Passed with `xelatex`; output `cover_example.pdf` is 1 page |
| Example cover-letter visual inspection | Passed; signature visible, no clipping |
| Example CV ATS extraction | Passed with `pdftotext -layout`; name, phone, email, headings, and reading order extract as text |
| Sanitized CV compile | Passed with `lualatex`; output `main_nimbus_analytics.pdf` is 2 pages |
| Sanitized cover-letter compile | Passed with `xelatex`; output `cover_nimbus_analytics_platform_engineer.pdf` is 1 page |
| Sanitized visual inspection | Passed; no clipped text, no broken icons, no orphaned role titles, signature visible |
| Sanitized ATS extraction | Passed; supported keywords present, unsupported Kubernetes/OpenTelemetry absent from CV experience |

Transient LaTeX files (`*.aux`, `*.log`, `*.out`, `*.fls`,
`*.fdb_latexmk`, `*.synctex.gz`) were cleaned from the temp verification tree
after inspection.

## Sanitized Workflow Result

The complete workflow was verified with fictional data only under
`%TEMP%\ai-job-search-production-verification-2026-07-12\sanitized-workflow`.
That location is outside the Git repository and cannot be committed by accident.

| Workflow stage | Result |
|---|---|
| `$job-setup` | Simulated Path C with fictional Avery Morgan profile and behavioral data |
| Sample job import | Created sanitized Nimbus Analytics posting and sample relocation deal-breaker posting |
| `$job-rank` | Ranked Nimbus as Strong Fit; excluded Far Harbor by location veto |
| `$job-apply` fit evaluation | Produced fit evaluation and salary lookup graceful skip because `salary_data.json` is absent |
| Confirmation gate | Proceeded only under the production-verification authorization for sanitized data |
| CV and cover generation | Created LaTeX drafts from supported fictional evidence only |
| Independent review | Delegated Codex reviewer found fixture-language and unsupported-label issues |
| Revision | Applied reviewer edits, then recompiled and rechecked ATS |
| Interview prep | Saved stage-specific phone-screen prep from submitted sanitized materials |
| Outcome tracking | Updated only the sample tracker row and sample archive |
| `$upskill-analysis` | Saved targeted upskill report for Kubernetes and OpenTelemetry gaps |

No real candidate documents, personal contact data, private employer history,
credentials, secrets, API keys, or salary data were used in the sanitized
workflow.

## Defects Found

1. `jobnet-search` defined `bun run test` but had no Bun test files. Fixed on the
   production-verification branch by adding
   `.agents/skills/jobnet-search/cli/tests/helpers.test.ts`.
2. `cv/main_example.tex` rendered `moderncv` achievement bullets clipped off the
   left page edge. Fixed on the production-verification branch by using
   `\cvlistitem{...}` inside `\cventry` blocks and documenting the rule in
   `.agents/skills/job-application-core/references/05-cv-templates.md`.
3. Added `tests/test_latex_template_contracts.py` so the clipping-prone LaTeX
   pattern is caught without requiring LaTeX in CI.

## Current Limitations

- The stable `codex-migration` branch is not yet updated with the production
  fixes. Production readiness is proven for the uncommitted
  `fix/production-verification-2026-07-12` working tree, not yet for the pushed
  stable branch.
- `python tools/check_upstream_updates.py --no-fetch` must be rerun after the
  fix branch is clean.
- MiKTeX still reports that updates have not been checked because repository
  host resolution failed during the package-database refresh attempt.
