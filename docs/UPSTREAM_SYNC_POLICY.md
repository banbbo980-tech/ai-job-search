# Upstream Sync Policy

This project has two important GitHub locations:

- `upstream` is the official project:
  `https://github.com/MadsLorentzen/ai-job-search.git`
- `origin` is the user's fork after it is created.

Think of `upstream` as the source we watch, and `origin` as the user's copy where
Codex work can be pushed. Never push to `upstream`.

## Branch Model

| Branch | Purpose |
|---|---|
| `upstream/master` | Official unmodified project history. |
| `origin/master` | Fork branch kept close to the official project when needed. |
| `codex-migration` | Stable Codex-native version for daily use. |
| `sync/upstream-<date>-<short-sha>` | Temporary branch for one official update. |

Do not merge official changes directly into `codex-migration`. Official updates
may include Claude-specific instructions, slash commands, or tool names. Those
must be converted by behavior into Codex skills, Codex subagent workflows, and
capability-based instructions before the stable branch changes.

## Update Flow

1. Start on `codex-migration`.
2. Make sure `git status --short` is clean.
3. Run:

```bash
python tools/check_upstream_updates.py
```

4. If updates exist, create a branch like:

```bash
git switch -c sync/upstream-2026-07-11-c134eef
```

5. Import the official changes into that branch.
6. Convert Claude-specific behavior into Codex-native behavior.
7. Run the full test suite and blocked-check review.
8. Save an update report under `docs/upstream-updates/`.
9. Ask the user before merging back into `codex-migration`.
10. Push only to `origin` after `python tools/security_guards.py` passes.

## Semantic Conversion Rules

| Official upstream change | Codex action |
|---|---|
| `CLAUDE.md` instructions changed | Apply relevant behavior to `AGENTS.md` and affected Codex skills. |
| `.claude/commands/*` changed | Update the corresponding `.agents/skills/*/SKILL.md` workflow. |
| `.claude/skills/*` changed | Update the matching Codex skill or shared reference. |
| New Claude slash command | Create a corresponding Codex skill. |
| Claude delegated-review behavior added | Convert to a Codex subagent workflow with a safe fallback. |
| Claude tool name changed | Convert to capability-based Codex instructions. |
| Portal CLI changed | Import and test the actual TypeScript/Bun changes. |
| Evaluation logic changed | Preserve the new official scoring behavior in Codex. |
| Template changed | Import and verify PDF layout and ATS behavior. |
| New official feature added | Implement full Codex-native feature parity. |
| Official feature removed | Report the impact and ask before removing it from Codex. |
| Documentation changed | Update Codex documentation without adding Claude requirements. |

## State File

`docs/upstream-state.json` records the last official commit that has been fully
converted and verified. Commit hashes, not dates, are the source of truth.

Update that file only after:

- the official change has been converted for Codex,
- required tests have passed or environment blocks are documented,
- the user has approved integration into `codex-migration`,
- the update report has been saved.

## Privacy Rule

Before every push, run:

```bash
python tools/security_guards.py
```

Do not push personal documents, CVs, generated applications, tracker rows,
salary data, secrets, credentials, or API keys.
