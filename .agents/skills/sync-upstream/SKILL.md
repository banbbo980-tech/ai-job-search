---
name: sync-upstream
description: Safely check, import, convert, test, and report official upstream ai-job-search updates for the Codex-native branch. Use when the user asks to sync with MadsLorentzen/ai-job-search, check upstream changes, prepare a sync branch, convert Claude-specific changes to Codex workflows, or verify feature parity before merging official updates.
---

# Sync Upstream

Use this skill to keep the Codex-native branch aligned with the official
project without reintroducing Claude Code or Anthropic API requirements.

## Required Preflight

1. Verify the repo root contains `AGENTS.md`, `.agents/skills/`, `CLAUDE.md`,
   `.claude/`, and `docs/upstream-state.json`.
2. Verify the worktree is clean with `git status --short`.
3. Verify the stable Codex branch is `codex-migration`.
4. Verify remotes:
   - `upstream` must point to `https://github.com/MadsLorentzen/ai-job-search.git`.
   - `origin` must point to the user's fork when configured.
5. Run the read-only checker:

```bash
python tools/check_upstream_updates.py
```

If the checker reports no updates, stop and report that result.

## Sync Workflow

When official updates exist:

1. Fetch `upstream`.
2. Compare `docs/upstream-state.json` `last_integrated_upstream_commit` with
   `upstream/master`.
3. Report official commits, changed files, deleted files, and Claude-specific
   files before editing.
4. Create a temporary branch named
   `sync/upstream-<date>-<official-short-sha>` from `codex-migration`.
5. Import official changes into the temporary branch only. Do not experiment on
   `codex-migration`.
6. Audit functionality changes before converting implementation details.
7. Convert by meaning and behavior:
   - `CLAUDE.md` changes -> `AGENTS.md` and affected Codex skills.
   - `.claude/commands/*` changes -> matching `.agents/skills/*/SKILL.md`.
   - `.claude/skills/*` changes -> matching Codex skill or shared reference.
   - New Claude slash command -> new Codex skill.
   - Claude delegated-review instructions -> Codex subagent workflow with the
     documented second-pass fallback.
   - Claude tool names -> capability-based Codex instructions.
   - Portal CLI changes -> import the TypeScript/Bun behavior and test it.
   - Evaluation changes -> preserve the official scoring behavior.
   - Template changes -> verify PDF layout and ATS extraction when tools exist.
   - New official feature -> implement Codex-native feature parity.
   - Removed official feature -> report impact and ask before removing Codex
     functionality.
8. Update tests and docs with the converted behavior.
9. Run full local verification:

```bash
python -m unittest discover -s tests -t . -v
python tools/lint_skills.py
python tools/security_guards.py
python tools/codex_compatibility.py
python tools/check_upstream_updates.py --no-fetch
```

10. Run Bun, LaTeX, and `pdftotext` checks when those tools are available.
    Report them as environment-blocked when unavailable.
11. Create `docs/upstream-updates/<date>_<official-short-sha>.md` with the
    parity table: official feature/change, official files, Codex equivalent,
    conversion performed, tests added or updated, verification result, and
    remaining risk.
12. Update `docs/upstream-state.json` only after conversion, tests, and user
    approval for integration.
13. Ask before merging the verified sync branch into `codex-migration`.
14. Push only to `origin`, never `upstream`, and never force-push.

## Safety Rules

- Never automatically delete existing Codex functionality because official
  upstream changed or removed a Claude file.
- Never push personal documents, CVs, application records, salary data,
  credentials, tokens, API keys, or generated private files.
- Run `python tools/security_guards.py` before every push.
- Preserve `CLAUDE.md` and `.claude/` until parity checks pass and the user
  approves removal.
- Do not install global software or change system-wide configuration without
  user approval.
