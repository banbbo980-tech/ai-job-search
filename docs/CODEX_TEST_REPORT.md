# Codex Test Report

Latest local verification for the Codex migration branch.

Branch: `codex-migration`

## Passed Checks

| Command | Result |
|---|---|
| `python tools/codex_compatibility.py` | `codex_compatibility: OK (12 workflow skills, 8 shared references, AGENTS.md)` |
| `python -m unittest discover -s tests -t . -v` | 68 tests passed |
| `python tools/lint_skills.py` | `lint_skills: OK (21 skills, 9 commands, settings.json)` |
| `python tools/security_guards.py` | `security_guards: OK (permissions allowlist, gitignore rules, package manifests)` |

## Environment-Blocked Checks

These checks require tools not currently available on this machine's PATH:

| Check | Command | Local status |
|---|---|---|
| Bun portal installs/typechecks/tests | `bun install`, `bun run typecheck`, `bun test --timeout 30000` in each portal CLI | Blocked when Bun is missing |
| CV LaTeX smoke | `cd cv && lualatex -interaction=nonstopmode -halt-on-error main_example.tex` | Blocked when `lualatex` is missing |
| Cover-letter LaTeX smoke | `cd cover_letters && xelatex -interaction=nonstopmode -halt-on-error cover_example.tex` | Blocked when `xelatex` is missing |
| ATS extraction | `pdftotext -layout cv/main_example.pdf cv/main_example.txt` | Blocked when Poppler is missing or PDFs cannot be compiled |

## Parity Notes

- Codex workflow skills preserve the original setup, search, rank, apply,
  reviewer, compile, ATS, interview, outcome, upskill, template, portal, and
  reset workflows.
- Sanitized fixtures under `tests/fixtures/` exercise the expected local data
  shapes without committing real personal information.
- Legacy `.claude/` files remain in the repo until final parity cleanup.
- Live portal requests were not automated in local tests, matching upstream CI's
  deliberate avoidance of live job-board traffic.
