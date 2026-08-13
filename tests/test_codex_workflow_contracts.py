import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / ".agents" / "skills"
FIXTURES = ROOT / "tests" / "fixtures"


def skill_text(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("`", ""))


class CodexWorkflowContractTests(unittest.TestCase):
    def test_sample_fixtures_are_sanitized(self):
        combined = "\n".join(path.read_text(encoding="utf-8") for path in FIXTURES.iterdir())
        self.assertIn("Example Candidate", combined)
        self.assertIn("candidate@example.com", combined)
        self.assertNotIn("EHSAN", combined.upper())
        self.assertNotIn("MadsLorentzen", combined)

    def test_sample_seen_jobs_schema_matches_search_and_rank_contracts(self):
        data = json.loads((FIXTURES / "sample_seen_jobs.json").read_text(encoding="utf-8"))
        self.assertIn("seen", data)
        entry = next(iter(data["seen"].values()))
        for key in ("title", "company", "url", "first_seen", "fit", "status"):
            self.assertIn(key, entry)

    def test_setup_preserves_three_onboarding_paths_and_confirmation(self):
        text = skill_text("job-setup")
        for phrase in [
            "Path A: read the documents folder",
            "Path B: import one pasted or attached CV/resume",
            "Path C: conduct an interview-style setup",
            "Present the full change set before writing",
            "Apply only confirmed changes",
        ]:
            self.assertIn(phrase, text)

    def test_search_preserves_portal_discovery_dedup_and_fallback(self):
        text = skill_text("job-search")
        flat = compact(text)
        for phrase in [
            "Discover portal skills",
            "Do not guess flags",
            "Deduplicate by canonical URL and case-insensitive company+title",
            "If Bun is unavailable",
        ]:
            self.assertIn(phrase, text)
        self.assertIn("Preserve fields added by $job-rank", flat)

    def test_rank_preserves_scoring_weights_and_vetoes(self):
        text = skill_text("job-rank")
        flat = compact(text)
        for phrase in [
            "technical 30%",
            "location deal-breakers as vetoes",
            "Never score from title alone",
        ]:
            self.assertIn(phrase, text)
        self.assertIn("experience 25%", flat)
        self.assertIn("behavioral 15%", flat)
        self.assertIn("career alignment 30%", flat)

    def test_apply_preserves_full_pipeline(self):
        text = skill_text("job-apply")
        for phrase in [
            "Evaluate Fit Before Drafting",
            "Should I proceed with drafting",
            "Independent Reviewer",
            "subagents are unavailable",
            "Compile and Inspect PDFs",
            "ATS Verification",
            "missing (gap)",
        ]:
            self.assertIn(phrase, text)

    def test_add_document_template_preserves_upstream_switch_and_cleanup(self):
        text = skill_text("add-document-template")
        for phrase in [
            "Switch Mode",
            "parent folder name exactly",
            "If more than one manifest matches",
            "Verify `template<source-extension>` exists",
            "Do not re-run registration",
            "`--use default` removes the managed block",
            "Exactly one managed block",
            "If activation was reached from Switch Mode",
            "_compile_test.fls",
            "_compile_test.fdb_latexmk",
            "_compile_test.synctex.gz",
            "any other",
            "_compile_test.*",
            "full compile command",
            "Source extension",
        ]:
            self.assertIn(phrase, text)

    def test_outcome_interview_upskill_and_reset_contracts(self):
        self.assertIn("do not overwrite", skill_text("application-outcome").lower())
        self.assertIn("what was actually submitted", skill_text("application-outcome"))
        self.assertIn("Do not invent examples", skill_text("interview-prep"))
        self.assertIn("Save", skill_text("upskill-analysis"))
        self.assertIn("exact confirmation text `RESET`", skill_text("reset-job-profile"))


if __name__ == "__main__":
    unittest.main()
