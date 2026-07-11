# Codex Production Checklist

Do not mark the project production-ready until every item is verified with
evidence.

## Git And Fork

- [ ] `codex-migration` is the active stable branch.
- [ ] `upstream` points to `https://github.com/MadsLorentzen/ai-job-search.git`.
- [ ] `origin` points to the user's GitHub fork.
- [ ] No push has been made to `upstream`.
- [ ] Fork visibility has been confirmed with the user.
- [ ] `python tools/security_guards.py` passes before push.

## Codex Parity

- [ ] Complete official feature parity for the recorded upstream commit.
- [ ] No active Claude Code runtime requirement.
- [ ] No Anthropic API key requirement.
- [ ] All Codex skills are discoverable.
- [ ] `AGENTS.md` applies from the repository root.
- [ ] Internal skill references resolve.
- [ ] Reviewer subagent workflow works when subagents are available.
- [ ] Second-pass reviewer fallback is documented and tested.
- [ ] Reset confirmation safeguards require exact confirmation.
- [ ] Personal files remain ignored by Git.

## Workflow Verification

- [ ] Candidate setup.
- [ ] Job search or sanitized sample-job import.
- [ ] Deduplication.
- [ ] Job ranking.
- [ ] Fit evaluation.
- [ ] User confirmation gate.
- [ ] CV generation.
- [ ] Cover-letter generation.
- [ ] Independent review.
- [ ] Revision.
- [ ] PDF compilation.
- [ ] Rendered PDF visual inspection.
- [ ] ATS extraction and reading-order verification.
- [ ] Supported-keyword verification.
- [ ] Interview preparation.
- [ ] Outcome recording.
- [ ] Upskill analysis.

## Tooling

- [ ] `python -m unittest discover -s tests -t . -v`.
- [ ] `python tools/lint_skills.py`.
- [ ] `python tools/security_guards.py`.
- [ ] `python tools/codex_compatibility.py`.
- [ ] `python tools/check_upstream_updates.py --no-fetch`.
- [ ] Bun portal checks for every portal CLI.
- [ ] LaTeX CV compile with `lualatex`.
- [ ] LaTeX cover-letter compile with `xelatex`.
- [ ] PDF page-count verification.
- [ ] `pdftotext` ATS extraction.
- [ ] Sanitized end-to-end workflow.

## Environment Status

As of the current local check:

- `gh` is not on PATH.
- `bun` is not on PATH.
- `lualatex` is not on PATH.
- `xelatex` is not on PATH.
- `pdftotext` is not on PATH.
- `winget` is available at
  `C:\Users\EHSAN COMPUTERS\AppData\Local\Microsoft\WindowsApps\winget.exe`.
- `scoop` and `choco` are not on PATH.

Blocked checks must stay marked blocked until the tools are installed and the
commands actually pass.

## Recommended Windows Prerequisites

Do not install anything here without user approval.

| Software | Why needed | Recommended install method | Source | Approximate disk use | Restart | Verify |
|---|---|---|---|---|---|---|
| GitHub CLI (`gh`) | Create/check the fork, authenticate safely, configure `origin`, and push. | `winget install --id GitHub.cli -e` or official MSI. | https://github.com/cli/cli | Usually under 100 MB. | New terminal usually enough. | `gh --version`, `gh auth status` |
| Bun | Official portal CLI install, typecheck, and test runner. | Official per-user PowerShell installer: `powershell -c "irm bun.sh/install.ps1|iex"`. | https://bun.sh/docs/installation | Usually under 200 MB before dependencies. Portal dependencies add more. | New terminal required after PATH update. | `bun --version`, `bun --revision` |
| MiKTeX | Provides `lualatex` and `xelatex` for CV and cover-letter PDFs. | Basic MiKTeX Installer, private per-user install, package install set to `Ask me first`. | https://miktex.org/howto/install-miktex | Basic installer is small; installed packages can grow from hundreds of MB to several GB. | Usually no reboot; new terminal may be needed. | `lualatex --version`, `xelatex --version` |
| Poppler for Windows | Provides `pdftotext` for ATS extraction and reading-order checks. | Portable ZIP from the Poppler Windows release, then add its `Library\bin` folder to the user PATH. | https://github.com/oschwartz10612/poppler-windows/releases | Usually tens to hundreds of MB extracted. | New terminal required after PATH update. | `pdftotext -v` |

Full production verification requires Bun portal tests, LaTeX compilation,
PDF page-count checks, rendered PDF visual inspection, `pdftotext` extraction,
ATS reading-order verification, supported-keyword verification, and a sanitized
end-to-end workflow.
