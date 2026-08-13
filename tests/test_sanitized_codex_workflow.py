import csv
import html
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


class SanitizedCodexWorkflowSmokeTest(unittest.TestCase):
    """Offline state-and-artifact smoke test for the conversational workflow.

    The skills are instruction contracts rather than a callable application, so
    this harness exercises their shared file lifecycle with fictional fixtures.
    External Gmail and Notion operations are represented by approved payloads.
    """

    def test_full_private_workflow_lifecycle(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            profile = shutil.copy(FIXTURES / "sample_candidate_profile.md", root / "profile.md")
            posting = shutil.copy(FIXTURES / "sample_job_posting.md", root / "posting.md")
            state_path = shutil.copy(FIXTURES / "sample_seen_jobs.json", root / "seen_jobs.json")

            self.assertIn("Example Candidate", Path(profile).read_text(encoding="utf-8"))
            posting_text = Path(posting).read_text(encoding="utf-8")
            self.assertIn("Example Climate Tools", posting_text)

            state = json.loads(Path(state_path).read_text(encoding="utf-8"))
            job = next(iter(state["seen"].values()))
            job.update(
                status="ranked",
                rank_score=78,
                rank_verdict="Strong Fit",
                strengths=["Verified Python and SQL evidence"],
                gaps=["dbt is preferred but unsupported"],
                eligibility_gate="UNVERIFIED",
                language_gate="PASS",
            )
            Path(state_path).write_text(json.dumps(state, indent=2), encoding="utf-8")

            application = root / "documents" / "applications" / "example-climate-tools_analytics-engineer"
            application.mkdir(parents=True)
            (application / "job_posting.md").write_text(posting_text, encoding="utf-8")
            (application / "cv_draft.tex").write_text("% fictional two-page CV source\n", encoding="utf-8")
            (application / "cover_letter.tex").write_text("% fictional one-page letter source\n", encoding="utf-8")
            (application / "application_form_fields.txt").write_text(
                "Motivation (18 words): Fictional evidence-backed answer for a fictional employer, measured for a sanitized application form field.\n",
                encoding="utf-8",
            )

            tracker = root / "job_search_tracker.csv"
            header = [
                "date", "company", "sector", "role", "role_type", "channel",
                "status", "contact_person", "fit_rating", "notes", "cv_file",
                "cover_letter_file", "source",
            ]
            row = [
                "2099-01-02", "Example Climate Tools", "Climate Tech",
                "Analytics Engineer", "Data", "Direct", "drafted", "", "78",
                "Sanitized draft", "cv/main_example-climate-tools_analytics-engineer.tex",
                "cover_letters/cover_example-climate-tools_analytics-engineer.tex",
                "https://example.com/jobs/analytics-engineer",
            ]
            with tracker.open("w", newline="", encoding="utf-8") as handle:
                csv.writer(handle).writerows([header, row])

            reviewer = {
                "method": "independent-reviewer-fixture",
                "unsupported_claims": [],
                "valid_revision": "Keep the verified Python evidence prominent",
            }
            (application / "review.json").write_text(json.dumps(reviewer), encoding="utf-8")
            (application / "interview_prep_screen.md").write_text(
                "# Fictional Interview Prep\n\nUse only archived claims.\n", encoding="utf-8"
            )
            (application / "outcome.md").write_text(
                "# Outcome: Example Climate Tools - Analytics Engineer\n\n**Status:** interview_only\n",
                encoding="utf-8",
            )
            (root / "upskill-report.md").write_text(
                "# Fictional Upskill Report\n\nGap: dbt (recorded, not invented).\n", encoding="utf-8"
            )

            gmail_proposal = {"company": row[1], "from": "drafted", "to": "interview"}
            self.assertEqual(row[6], "drafted")
            row[6] = gmail_proposal["to"]  # represents explicit fixture approval

            notion_payload = {"company": row[1], "role": row[3], "status": row[6]}
            self.assertNotIn("cv_content", notion_payload)
            self.assertNotIn("cover_letter_content", notion_payload)

            escaped_company = html.escape(row[1], quote=True)
            report = root / "report.html"
            report.write_text(
                f"<!doctype html><title>Fictional pipeline</title><h1>{escaped_company}</h1>",
                encoding="utf-8",
            )

            self.assertEqual(job["status"], "ranked")
            self.assertTrue((application / "job_posting.md").is_file())
            self.assertTrue((application / "application_form_fields.txt").is_file())
            self.assertEqual(notion_payload["status"], "interview")
            self.assertIn("Fictional pipeline", report.read_text(encoding="utf-8"))
            self.assertNotIn("EHSAN", "\n".join(p.read_text(encoding="utf-8") for p in root.rglob("*.*")).upper())


if __name__ == "__main__":
    unittest.main()
