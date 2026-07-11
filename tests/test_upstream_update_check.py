import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHECK_SCRIPT = REPO_ROOT / "tools" / "check_upstream_updates.py"

sys.path.insert(0, str(REPO_ROOT / "tools"))
import check_upstream_updates  # noqa: E402


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)
    return result.stdout.strip()


def write_file(root: Path, relpath: str, text: str) -> None:
    path = root / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def commit_all(repo: Path, message: str) -> str:
    git(repo, "add", "--all")
    git(repo, "commit", "-m", message)
    return git(repo, "rev-parse", "HEAD")


class UpstreamFixture(unittest.TestCase):
    def setUp(self):
        self.tempdir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tempdir, ignore_errors=True)

    def make_fixture(self, initial_files=None):
        initial_files = initial_files or {}
        official = self.tempdir / "official"
        work = self.tempdir / "work"

        official.mkdir()
        subprocess.run(["git", "-C", str(official), "init"], check=True, capture_output=True, text=True)
        git(official, "config", "user.name", "Test User")
        git(official, "config", "user.email", "test@example.com")
        write_file(official, "README.md", "# official\n")
        for relpath, text in initial_files.items():
            write_file(official, relpath, text)
        base = commit_all(official, "base")
        git(official, "branch", "-M", "master")

        subprocess.run(["git", "clone", str(official), str(work)], check=True, capture_output=True, text=True)
        git(work, "remote", "rename", "origin", "upstream")
        git(work, "checkout", "-b", "codex-migration")
        git(work, "config", "user.name", "Codex")
        git(work, "config", "user.email", "codex@example.com")
        self.write_state(work, official, base)
        commit_all(work, "state")
        return official, work, base

    def write_state(self, work: Path, official: Path, commit: str) -> None:
        write_file(
            work,
            "docs/upstream-state.json",
            json.dumps(
                {
                    "schema_version": 1,
                    "official_repository_url": str(official),
                    "last_integrated_upstream_commit": commit,
                    "integration_date": "2026-07-11",
                    "codex_branch": "codex-migration",
                    "parity_test_status": "passed",
                    "migration_report_path": "docs/CODEX_TEST_REPORT.md",
                },
                indent=2,
            ),
        )

    def official_commit(self, official: Path, relpath: str, text: str, message: str) -> str:
        write_file(official, relpath, text)
        return commit_all(official, message)

    def delete_official_file(self, official: Path, relpath: str, message: str) -> str:
        (official / relpath).unlink()
        return commit_all(official, message)

    def run_checker(self, work: Path):
        return subprocess.run(
            [
                sys.executable,
                str(CHECK_SCRIPT),
                "--repo",
                str(work),
                "--state",
                str(work / "docs" / "upstream-state.json"),
                "--no-fetch",
                "--json",
            ],
            capture_output=True,
            text=True,
        )

    def fetch(self, work: Path) -> None:
        git(work, "fetch", "upstream")


class StateFileTests(unittest.TestCase):
    def test_repo_state_file_has_required_schema(self):
        state = check_upstream_updates.load_state(REPO_ROOT / "docs" / "upstream-state.json")
        self.assertEqual(state["schema_version"], 1)
        self.assertEqual(
            state["official_repository_url"],
            "https://github.com/MadsLorentzen/ai-job-search",
        )
        self.assertRegex(state["last_integrated_upstream_commit"], r"^[0-9a-f]{40}$")
        self.assertEqual(state["codex_branch"], "codex-migration")
        self.assertTrue(state["migration_report_path"].endswith(".md"))


class UpdateCheckTests(UpstreamFixture):
    def test_no_update_available(self):
        _, work, _ = self.make_fixture()
        result = self.run_checker(work)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertFalse(report["updates_available"])
        self.assertEqual(report["status"], "up_to_date")

    def test_normal_official_update(self):
        official, work, _ = self.make_fixture()
        self.official_commit(official, "README.md", "# official\n\nchanged\n", "readme update")
        self.fetch(work)

        result = self.run_checker(work)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report["updates_available"])
        self.assertEqual(report["commit_count"], 1)
        self.assertEqual(report["changed_files"][0]["paths"], ["README.md"])

    def test_sync_update_branch_is_allowed(self):
        _, work, _ = self.make_fixture()
        git(work, "checkout", "-b", "sync/upstream-2026-07-12-abcdef0")

        result = self.run_checker(work)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["branch"], "sync/upstream-2026-07-12-abcdef0")

    def test_non_sync_feature_branch_fails_safely(self):
        _, work, _ = self.make_fixture()
        git(work, "checkout", "-b", "feature/random")

        result = self.run_checker(work)
        self.assertEqual(result.returncode, 1)
        self.assertIn("expected stable Codex branch", result.stdout)
        self.assertIn("sync/upstream-YYYY-MM-DD", result.stdout)

    def test_new_claude_command_is_highlighted(self):
        official, work, _ = self.make_fixture()
        self.official_commit(official, ".claude/commands/new.md", "# /new\n", "new claude command")
        self.fetch(work)

        result = self.run_checker(work)
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("claude-command", report["changed_files"][0]["categories"])
        self.assertEqual(len(report["claude_specific_changes"]), 1)

    def test_changed_claude_skill_is_highlighted(self):
        official, work, _ = self.make_fixture(
            {".claude/skills/reviewer/SKILL.md": "---\nname: reviewer\ndescription: test\n---\n"}
        )
        self.official_commit(
            official,
            ".claude/skills/reviewer/SKILL.md",
            "---\nname: reviewer\ndescription: changed\n---\n",
            "change claude skill",
        )
        self.fetch(work)

        result = self.run_checker(work)
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("claude-skill", report["changed_files"][0]["categories"])
        self.assertEqual(len(report["claude_specific_changes"]), 1)

    def test_new_portal_integration_is_highlighted(self):
        official, work, _ = self.make_fixture()
        self.official_commit(
            official,
            ".agents/skills/example-search/cli/src/cli.ts",
            "console.log('search')\n",
            "add portal cli",
        )
        self.fetch(work)

        result = self.run_checker(work)
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("portal-integration", report["changed_files"][0]["categories"])

    def test_deleted_official_feature_is_highlighted(self):
        official, work, _ = self.make_fixture({"feature.md": "# feature\n"})
        self.delete_official_file(official, "feature.md", "remove feature")
        self.fetch(work)

        result = self.run_checker(work)
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(report["changed_files"][0]["status"], "D")
        self.assertIn("deleted-official-feature", report["changed_files"][0]["categories"])

    def test_missing_state_file_fails_safely(self):
        _, work, _ = self.make_fixture()
        (work / "docs" / "upstream-state.json").unlink()
        commit_all(work, "remove state")

        result = self.run_checker(work)
        self.assertEqual(result.returncode, 1)
        self.assertIn("state file is missing", result.stdout)

    def test_malformed_state_file_fails_safely(self):
        _, work, _ = self.make_fixture()
        write_file(work, "docs/upstream-state.json", "{bad json")
        commit_all(work, "break state")

        result = self.run_checker(work)
        self.assertEqual(result.returncode, 1)
        self.assertIn("state file is malformed JSON", result.stdout)

    def test_missing_upstream_remote_fails_safely(self):
        _, work, _ = self.make_fixture()
        git(work, "remote", "remove", "upstream")

        result = self.run_checker(work)
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing required 'upstream' remote", result.stdout)

    def test_dirty_working_tree_fails_safely(self):
        _, work, _ = self.make_fixture()
        write_file(work, "README.md", "# dirty\n")

        result = self.run_checker(work)
        self.assertEqual(result.returncode, 1)
        self.assertIn("working tree is dirty", result.stdout)


if __name__ == "__main__":
    unittest.main()
