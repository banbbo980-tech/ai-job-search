import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class LatexTemplateContractTests(unittest.TestCase):
    def cventry_blocks(self, text: str):
        start = 0
        command = "\\cventry"
        while True:
            start = text.find(command, start)
            if start == -1:
                return

            index = start + len(command)
            brace_depth = 0
            groups_closed = 0
            while index < len(text):
                char = text[index]
                if char == "{":
                    brace_depth += 1
                elif char == "}":
                    brace_depth -= 1
                    if brace_depth == 0:
                        groups_closed += 1
                        if groups_closed == 6:
                            yield text[start : index + 1]
                            start = index + 1
                            break
                index += 1
            else:
                return

    def test_moderncv_cventry_blocks_use_layout_safe_bullets(self):
        """Nested list indentation clips moderncv cventry bullets in rendered PDFs."""
        checked_paths = [
            ROOT / "cv" / "main_example.tex",
            ROOT
            / ".agents"
            / "skills"
            / "job-application-core"
            / "references"
            / "05-cv-templates.md",
        ]
        pattern = re.compile(r"\\item\s*\{\s*\\cventry")

        for path in checked_paths:
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                self.assertNotRegex(text, pattern)
                for block in self.cventry_blocks(text):
                    self.assertNotIn(r"\begin{itemize}", block)

    def test_example_cv_uses_ats_safe_moderncv_symbols(self):
        """Moderncv icons can extract as private-use glyphs in ATS text."""
        text = (ROOT / "cv" / "main_example.tex").read_text(encoding="utf-8")

        self.assertIn(r"\renewcommand*{\mobilephonesymbol}{Phone:~}", text)
        self.assertIn(r"\renewcommand*{\emailsymbol}{Email:~}", text)
        self.assertIn(r"\renewcommand*{\labelitemi}{\strut\textcolor{color1}{-}}", text)
        self.assertIn(r"\renewcommand*{\listitemsymbol}{\labelitemi~}", text)


if __name__ == "__main__":
    unittest.main()
