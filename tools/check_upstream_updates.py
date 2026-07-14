#!/usr/bin/env python3
"""Read-only upstream update checker for the Codex migration branch.

The checker fetches or inspects `upstream/master`, compares it with
docs/upstream-state.json, and reports what would need conversion. It never
merges, commits, or pushes.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STATE = ROOT / "docs" / "upstream-state.json"
UPSTREAM_REMOTE = "upstream"
UPSTREAM_BRANCH = "master"
HEX_RE = re.compile(r"^[0-9a-f]{40}$", re.I)
SYNC_BRANCH_RE = re.compile(r"^sync/upstream-\d{4}-\d{2}-\d{2}-[0-9a-f]{7,40}$", re.I)
FRAMEWORK_SKILL_DIR = ".claude/skills/job-application-assistant"
FRAMEWORK_FILES = [
    "01-candidate-profile.md",
    "02-behavioral-profile.md",
    "03-writing-style.md",
    "04-job-evaluation.md",
    "05-cv-templates.md",
    "06-cover-letter-templates.md",
    "07-interview-prep.md",
    "SKILL.md",
]


class SafeError(RuntimeError):
    """An expected safety stop with a user-facing message."""


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise SafeError(f"git {' '.join(args)} failed: {detail}")
    return result


def normalize_url(url: str) -> str:
    url = url.strip().rstrip("/")
    if url.endswith(".git"):
        url = url[:-4]
    return url


def load_state(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SafeError(f"state file is missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SafeError(f"state file is malformed JSON: {exc}") from exc

    required = {
        "schema_version": int,
        "official_repository_url": str,
        "last_integrated_upstream_commit": str,
        "integration_date": str,
        "codex_branch": str,
        "parity_test_status": str,
        "migration_report_path": str,
    }
    for key, expected_type in required.items():
        value = data.get(key)
        if not isinstance(value, expected_type):
            raise SafeError(f"state file field {key!r} must be {expected_type.__name__}")

    if data["schema_version"] != 1:
        raise SafeError("state file schema_version must be 1")
    if not HEX_RE.match(data["last_integrated_upstream_commit"]):
        raise SafeError("state file last_integrated_upstream_commit must be a full 40-character commit hash")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", data["integration_date"]):
        raise SafeError("state file integration_date must use YYYY-MM-DD")
    return data


def ensure_clean(repo: Path) -> None:
    status = git(repo, "status", "--porcelain").stdout.strip()
    if status:
        raise SafeError("working tree is dirty; commit or stash local changes before checking upstream updates")


def ensure_branch(repo: Path, expected_branch: str) -> str:
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if branch != expected_branch and not SYNC_BRANCH_RE.match(branch):
        raise SafeError(
            f"current branch is {branch!r}; expected stable Codex branch {expected_branch!r} "
            "or a sync/upstream-YYYY-MM-DD-<sha> update branch"
        )
    return branch


def ensure_upstream(repo: Path, expected_url: str) -> str:
    result = git(repo, "remote", "get-url", UPSTREAM_REMOTE, check=False)
    if result.returncode != 0:
        raise SafeError("missing required 'upstream' remote")
    remote_url = result.stdout.strip()
    if expected_url and normalize_url(remote_url) != normalize_url(expected_url):
        raise SafeError(
            "upstream remote does not match docs/upstream-state.json: "
            f"{remote_url!r} != {expected_url!r}"
        )
    return remote_url


def ensure_commit_exists(repo: Path, commit: str) -> None:
    result = git(repo, "cat-file", "-e", f"{commit}^{{commit}}", check=False)
    if result.returncode != 0:
        raise SafeError(f"recorded upstream commit is not present locally: {commit}")


def ensure_ancestor(repo: Path, older: str, newer: str) -> None:
    result = git(repo, "merge-base", "--is-ancestor", older, newer, check=False)
    if result.returncode != 0:
        raise SafeError(
            "recorded upstream commit is not an ancestor of upstream/master; "
            "review history before syncing"
        )


def change_categories(status: str, paths: list[str]) -> list[str]:
    categories: list[str] = []
    if status.startswith("D"):
        categories.append("deleted-official-feature")
    for path in paths:
        if path == "CLAUDE.md":
            categories.append("claude-instructions")
        elif path.startswith(".claude/commands/"):
            categories.append("claude-command")
        elif path.startswith(".claude/skills/"):
            categories.append("claude-skill")
        elif (path.startswith(".agents/skills/") and "/cli/" in path) or path.startswith("job_scraper/"):
            categories.append("portal-integration")
        elif path.startswith(("cv/", "cover_letters/", "templates/")):
            categories.append("document-template")
        elif path.startswith(("README", "docs/", "SETUP", "CONTRIBUTING")):
            categories.append("documentation")
        elif path.startswith("tests/"):
            categories.append("test")
    return sorted(set(categories))


def parse_name_status(raw: str) -> list[dict[str, Any]]:
    changes: list[dict[str, Any]] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0]
        paths = parts[1:]
        categories = change_categories(status, paths)
        changes.append(
            {
                "status": status,
                "paths": paths,
                "categories": categories,
                "claude_specific": any(category.startswith("claude-") for category in categories),
            }
        )
    return changes


def get_framework_version_from_text(text: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        if key.strip() == "framework_version":
            return value.strip().strip('"').strip("'")
    return None


def parse_semver(version: str) -> tuple[int, int, int]:
    match = re.match(r"^v?(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        return (0, 0, 0)
    return tuple(int(part) for part in match.groups())


def compare_framework_versions(repo: Path, upstream_ref: str) -> list[dict[str, str | None]]:
    updates: list[dict[str, str | None]] = []
    for filename in FRAMEWORK_FILES:
        rel_path = f"{FRAMEWORK_SKILL_DIR}/{filename}"
        local_path = repo / rel_path
        local_version = None
        if local_path.exists():
            local_version = get_framework_version_from_text(local_path.read_text(encoding="utf-8"))

        upstream_result = git(repo, "show", f"{upstream_ref}:{rel_path}", check=False)
        if upstream_result.returncode != 0:
            continue
        upstream_version = get_framework_version_from_text(upstream_result.stdout)
        if not upstream_version:
            continue

        if not local_version or parse_semver(upstream_version) > parse_semver(local_version):
            updates.append(
                {
                    "path": rel_path,
                    "local": local_version,
                    "upstream": upstream_version,
                }
            )
    return updates


def check_updates(repo: Path, state_path: Path, fetch: bool = True) -> dict[str, Any]:
    repo = repo.resolve()
    state_path = state_path.resolve()
    state = load_state(state_path)

    ensure_clean(repo)
    branch = ensure_branch(repo, state["codex_branch"])
    remote_url = ensure_upstream(repo, state["official_repository_url"])

    if fetch:
        git(repo, "fetch", "--prune", UPSTREAM_REMOTE)

    upstream_ref = f"{UPSTREAM_REMOTE}/{UPSTREAM_BRANCH}"
    upstream_commit = git(repo, "rev-parse", upstream_ref).stdout.strip()
    recorded_commit = state["last_integrated_upstream_commit"]
    ensure_commit_exists(repo, recorded_commit)
    ensure_ancestor(repo, recorded_commit, upstream_commit)

    if recorded_commit == upstream_commit:
        commits: list[str] = []
        changes: list[dict[str, Any]] = []
    else:
        commits = git(repo, "log", "--oneline", f"{recorded_commit}..{upstream_ref}").stdout.splitlines()
        raw_changes = git(repo, "diff", "--name-status", recorded_commit, upstream_ref).stdout
        changes = parse_name_status(raw_changes)
    framework_version_updates = compare_framework_versions(repo, upstream_ref)

    short = upstream_commit[:7]
    today = _dt.date.today().isoformat()
    updates_available = recorded_commit != upstream_commit
    return {
        "status": "updates_available" if updates_available else "up_to_date",
        "updates_available": updates_available,
        "repo": str(repo),
        "state_file": str(state_path),
        "branch": branch,
        "upstream_remote": remote_url,
        "recorded_commit": recorded_commit,
        "upstream_ref": upstream_ref,
        "upstream_commit": upstream_commit,
        "commit_count": len(commits),
        "file_change_count": len(changes),
        "commits": commits,
        "changed_files": changes,
        "claude_specific_changes": [change for change in changes if change["claude_specific"]],
        "framework_version_updates": framework_version_updates,
        "recommended_sync_branch": f"sync/upstream-{today}-{short}" if updates_available else None,
    }


def print_text(report: dict[str, Any]) -> None:
    print("Upstream update check")
    print(f"Repository: {report['repo']}")
    print(f"Current branch: {report['branch']}")
    print(f"Upstream remote: {report['upstream_remote']}")
    print(f"Recorded official commit: {report['recorded_commit']}")
    print(f"Current upstream/master: {report['upstream_commit']}")

    if not report["updates_available"]:
        print("Status: up to date; no official updates are available.")
        return

    print(
        "Status: updates available "
        f"({report['commit_count']} commit(s), {report['file_change_count']} file change(s))."
    )
    print(f"Recommended sync branch: {report['recommended_sync_branch']}")
    print("\nOfficial commits:")
    for commit in report["commits"]:
        print(f"- {commit}")

    print("\nChanged official files:")
    for change in report["changed_files"]:
        path_text = " -> ".join(change["paths"])
        categories = ", ".join(change["categories"]) or "general"
        print(f"- {change['status']} {path_text} [{categories}]")

    if report["claude_specific_changes"]:
        print("\nClaude-specific changes requiring semantic Codex conversion:")
        for change in report["claude_specific_changes"]:
            print(f"- {' -> '.join(change['paths'])}")

    if report["framework_version_updates"]:
        print("\nFramework version markers newer upstream:")
        for update in report["framework_version_updates"]:
            print(f"- {update['path']}: local {update['local']} < upstream {update['upstream']}")

    print("\nNext safe step: create the sync branch, import changes there, convert behavior, test parity, and ask before merging.")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT, help="Repository root to inspect")
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE, help="Path to upstream-state.json")
    parser.add_argument("--no-fetch", action="store_true", help="Inspect existing upstream/master without network fetch")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        report = check_updates(args.repo, args.state, fetch=not args.no_fetch)
    except SafeError as exc:
        if args.json:
            print(json.dumps({"status": "safe_error", "error": str(exc)}, indent=2))
        else:
            print(f"check_upstream_updates: safe stop: {exc}")
        return 1

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_text(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
