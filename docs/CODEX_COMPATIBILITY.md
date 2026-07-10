# Codex Compatibility

AI Job Search now has Codex-native workflow skills under `.agents/skills/` and
root guidance in `AGENTS.md`.

## Supported Codex Surfaces

| Surface | Support | Notes |
|---|---|---|
| Codex CLI | Supported | Best local-first path for filesystem, Python, Bun, LaTeX, and PDF tooling. |
| ChatGPT desktop app with local project | Supported | Works when the local project exposes file and command execution. |
| ChatGPT Work | Supported with environment limits | Local filesystem, command execution, subagents, and network access may depend on workspace policy. |

## Skill Discovery

Codex skills live under `.agents/skills/`:

- Workflow skills: `$job-setup`, `$job-search`, `$job-rank`, `$job-apply`,
  `$profile-expand`, `$interview-prep`, `$application-outcome`,
  `$upskill-analysis`, `$add-document-template`, `$add-job-portal`,
  `$reset-job-profile`.
- Shared references: `$job-application-core`.
- Portal skills: `jobindex-search`, `jobnet-search`, `jobbank-search`,
  `jobdanmark-search`, `linkedin-search`, `freehire-search`.

Legacy `CLAUDE.md` and `.claude/` are retained for parity comparison and should
not be used as the active Codex entry points.

## Environment Dependencies

| Dependency | Required for | Graceful fallback |
|---|---|---|
| Python 3.10+ | salary tools, lint, tests | No |
| Bun | portal CLIs | `$job-search` can use web fallback, but portal CLI checks are blocked |
| LaTeX `lualatex` | CV PDF compilation | `.tex` drafts can be produced, PDF verification blocked |
| LaTeX `xelatex` | cover-letter PDF compilation | `.tex` drafts can be produced, PDF verification blocked |
| Poppler `pdftotext` | ATS text-layer verification | reduced visual keyword review |
| Network/web access | live portals, company research, resource research | user can paste postings; research steps report blocked |
| Subagents | independent reviewer and rank batching | documented second-pass fallback |

## Preserved Legacy Coverage

The migration keeps CI coverage for:

- Python unit tests.
- Skill/command lint.
- Security guards.
- Portal TypeScript checks.
- LaTeX smoke compiles.

Local environments without Bun, LaTeX, or Poppler must report those checks as
environment-blocked, not passing.

## Active Compatibility Check

Run:

```bash
python tools/codex_compatibility.py
```

This verifies:

- `AGENTS.md` exists with required Codex guidance.
- All required Codex workflow skills exist.
- Skill names and descriptions are unique and non-placeholder.
- Shared references exist.
- Active Codex workflows do not require the `claude` executable or an Anthropic
  API key.
- `$job-apply` preserves reviewer fallback, compile, and ATS contracts.
- `$reset-job-profile` preserves exact `RESET` confirmation.
- Personal-data `.gitignore` protections remain present.
