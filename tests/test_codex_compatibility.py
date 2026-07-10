import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class CodexCompatibilityTests(unittest.TestCase):
    def test_codex_compatibility_script_passes(self):
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "tools" / "codex_compatibility.py")],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("codex_compatibility: OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
