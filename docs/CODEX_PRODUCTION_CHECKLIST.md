# Codex Production Checklist

Do not mark the pushed stable branch production-ready until every required item
is verified with evidence and the production-verification fixes are reviewed.

## Git And Fork

- [ ] `codex-migration` is the active stable branch.
- [x] `upstream` points to `https://github.com/MadsLorentzen/ai-job-search.git`.
- [x] `origin` points to the user's GitHub fork.
- [x] No push was made to `upstream`.
- [x] Fork visibility was previously confirmed during migration push
  verification.
- [x] `python tools/security_guards.py` passes.
- [ ] Production-verification fixes are committed, merged, and pushed only after
  user approval.

## Codex Parity

- [x] Complete official feature parity for recorded upstream commit `8bee3dd`.
- [x] No active Claude Code runtime requirement.
- [x] No Anthropic API key requirement.
- [x] All Codex skills are discoverable.
- [x] `AGENTS.md` applies from the repository root.
- [x] Internal skill references resolve.
- [x] Reviewer subagent workflow works when subagents are available.
- [x] Second-pass reviewer fallback is documented in `$job-apply`.
- [x] Reset confirmation safeguards require exact confirmation.
- [x] Personal files remain ignored by Git.

## Workflow Verification

- [x] Candidate setup, using sanitized sample data only.
- [x] Job search or sanitized sample-job import.
- [x] Deduplication and seen-job state shape.
- [x] Job ranking.
- [x] Location deal-breaker handling.
- [x] Fit evaluation.
- [x] User confirmation gate, simulated by explicit production-verification
  authorization for sanitized data.
- [x] CV generation.
- [x] Cover-letter generation.
- [x] Independent review by delegated Codex subagent.
- [x] Reviewer fallback remains documented.
- [x] Revision.
- [x] PDF compilation.
- [x] Rendered PDF visual inspection.
- [x] ATS extraction and reading-order verification.
- [x] Supported-keyword verification.
- [x] Interview preparation.
- [x] Outcome recording.
- [x] Upskill analysis.
- [x] Optional salary lookup skips safely when `salary_data.json` is absent.

## Tooling

- [x] `python -m unittest discover -s tests -t . -v` passed: 88 tests.
- [x] `python tools/lint_skills.py` passed.
- [x] `python tools/security_guards.py` passed.
- [x] `python tools/codex_compatibility.py` passed.
- [ ] `python tools/check_upstream_updates.py --no-fetch` rerun on a clean
  working tree. Current result is a safe stop because the fix branch has
  intentional uncommitted changes.
- [x] Bun portal install, typecheck, and test checks passed for all six portal
  CLIs.
- [x] LaTeX CV compile with `lualatex`.
- [x] LaTeX cover-letter compile with `xelatex`.
- [x] PDF page-count verification.
- [x] `pdftotext` ATS extraction.
- [x] Sanitized end-to-end workflow.

## Environment Status

As of 2026-07-12:

- Bun `1.3.14+0d9b296af` is installed at
  `%USERPROFILE%\.bun\bin\bun.exe`.
- MiKTeX `25.12` is installed for the current user at
  `%LOCALAPPDATA%\Programs\MiKTeX`.
- Poppler `26.02.0` is installed at
  `%LOCALAPPDATA%\Programs\poppler-26.02.0-0`.
- MiKTeX's `titlesec` package was installed because `cover.cls` requires
  `titlesec.sty`.
- MiKTeX package database refresh failed with `Couldn't resolve host name`; the
  compilers still completed all required local document checks.
- `gh` was not installed during this phase because Git Credential Manager was
  already used for the authorized push workflow.

## Verified Windows Prerequisites

| Software | Why needed | Installed method | Source | Verify |
|---|---|---|---|---|
| Bun | Portal CLI installs, typechecks, and tests. | Official per-user PowerShell installer. | `https://bun.com/docs/installation` | `bun --version`, `bun --revision`, `where.exe bun` |
| MiKTeX | `lualatex` and `xelatex` for CV and cover-letter PDFs. | Official Basic MiKTeX Installer, private per-user install. | `https://miktex.org/download` | `lualatex --version`, `xelatex --version`, `where.exe lualatex`, `where.exe xelatex` |
| Poppler for Windows | `pdftotext`, `pdfinfo`, and `pdftoppm` for ATS/page-count/render checks. | Portable ZIP from project-documented Poppler Windows release, then user PATH update. | `https://github.com/oschwartz10612/poppler-windows/releases` | `pdftotext -v`, `pdfinfo -v`, `pdftoppm -v`, `where.exe pdftotext` |

## Current Production Readiness

The production-verification branch has passed all available functional checks
except the upstream-state checker, which is blocked by the intentionally dirty
working tree. The pushed `codex-migration` branch should not be called
production-ready until the fixes are reviewed, committed, merged, pushed, and
the upstream-state checker passes again on a clean tree.
