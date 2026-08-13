"""Additional regressions for the state-aware Codex upstream checker.

Upstream's stock checker falls back from a missing ``upstream`` remote to
``origin``. This fork deliberately fails closed instead: origin is the user's
public fork and is not evidence of official state. These tests preserve the
useful upstream URL and missing-file regressions under that stricter contract.
"""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "tools" / "check_upstream_updates.py"
TEMPLATE_URL = "https://github.com/MadsLorentzen/ai-job-search.git"
FORK_URL = "https://github.com/octocat/ai-job-search.git"

FRAMEWORK_FILES = [
    ".claude/skills/job-application-assistant/01-candidate-profile.md",
    ".claude/skills/job-application-assistant/02-behavioral-profile.md",
    ".claude/skills/job-application-assistant/03-writing-style.md",
    ".claude/skills/job-application-assistant/04-job-evaluation.md",
    ".claude/skills/job-application-assistant/05-cv-templates.md",
    ".claude/skills/job-application-assistant/06-cover-letter-templates.md",
    ".claude/skills/job-application-assistant/07-interview-prep.md",
    ".claude/skills/job-application-assistant/08-application-forms.md",
    ".claude/skills/job-application-assistant/09-web-research.md",
    ".claude/skills/job-application-assistant/SKILL.md",
    "AGENTS.md",
]
FRONTMATTER = "---\nframework_version: 1.0.0\n---\n"


def run_git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True
    )
    if result.returncode:
        raise AssertionError(result.stdout + result.stderr)
    return result.stdout.strip()


class StateAwareCheckerFixture(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        tools = self.root / "tools"
        tools.mkdir()
        shutil.copy(SCRIPT, tools / "check_upstream_updates.py")

        for rel in FRAMEWORK_FILES:
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(FRONTMATTER, encoding="utf-8")

        subprocess.run(
            ["git", "init", "-b", "master"], cwd=self.root,
            check=True, capture_output=True,
        )
        run_git(self.root, "config", "user.name", "Test")
        run_git(self.root, "config", "user.email", "test@example.com")
        run_git(self.root, "add", "-A")
        run_git(self.root, "commit", "-m", "framework base")
        self.base = run_git(self.root, "rev-parse", "HEAD")

        state = {
            "schema_version": 1,
            "official_repository_url": TEMPLATE_URL.removesuffix(".git"),
            "last_integrated_upstream_commit": self.base,
            "integration_date": "2026-08-13",
            "codex_branch": "master",
            "parity_test_status": "fixture",
            "migration_report_path": "docs/fixture.md",
        }
        state_path = self.root / "docs" / "upstream-state.json"
        state_path.parent.mkdir(parents=True)
        state_path.write_text(json.dumps(state), encoding="utf-8")
        run_git(self.root, "add", "-A")
        run_git(self.root, "commit", "-m", "add Codex state")
        self.state_path = state_path

    def add_remote(self, name: str, url: str) -> None:
        run_git(self.root, "remote", "add", name, url)

    def set_remote_ref(self, name: str, commit: str) -> None:
        run_git(self.root, "update-ref", f"refs/remotes/{name}/master", commit)

    def run_checker(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(self.root / "tools" / "check_upstream_updates.py"),
                "--repo", str(self.root),
                "--state", str(self.state_path),
                "--no-fetch",
                *args,
            ],
            cwd=self.root,
            capture_output=True,
            text=True,
        )


class RemoteSafetyTests(StateAwareCheckerFixture):
    def test_fork_origin_is_never_used_as_official_fallback(self):
        self.add_remote("origin", FORK_URL)
        self.set_remote_ref("origin", self.base)
        result = self.run_checker()
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing required 'upstream' remote", result.stdout)

    def test_wrong_upstream_remote_fails_closed(self):
        self.add_remote("upstream", FORK_URL)
        self.set_remote_ref("upstream", self.base)
        result = self.run_checker()
        self.assertEqual(result.returncode, 1)
        self.assertIn("does not match", result.stdout)

    def test_lowercased_official_url_is_accepted(self):
        self.add_remote("upstream", TEMPLATE_URL.lower())
        self.set_remote_ref("upstream", self.base)
        result = self.run_checker("--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "up_to_date")

    def test_explicit_official_upstream_is_used(self):
        self.add_remote("origin", FORK_URL)
        self.add_remote("upstream", TEMPLATE_URL)
        self.set_remote_ref("upstream", self.base)
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Status: up to date", result.stdout)
        self.assertIn("Upstream remote", result.stdout)


class MissingFrameworkFileTests(StateAwareCheckerFixture):
    def test_file_missing_upstream_is_reported_instead_of_silent_ok(self):
        self.add_remote("upstream", TEMPLATE_URL)
        run_git(self.root, "rm", "AGENTS.md")
        run_git(self.root, "commit", "-m", "upstream drops AGENTS")
        upstream_drop = run_git(self.root, "rev-parse", "HEAD")
        self.set_remote_ref("upstream", upstream_drop)

        (self.root / "AGENTS.md").write_text(FRONTMATTER, encoding="utf-8")
        run_git(self.root, "add", "AGENTS.md")
        run_git(self.root, "commit", "-m", "fork retains AGENTS")

        result = self.run_checker("--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertIn("AGENTS.md", report["framework_files_missing_upstream"])


if __name__ == "__main__":
    unittest.main()
