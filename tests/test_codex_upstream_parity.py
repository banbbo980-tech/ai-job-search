import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"
CORE = SKILLS / "job-application-core" / "references"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class NewCodexWorkflowTests(unittest.TestCase):
    def test_new_integrations_are_complete_skills(self):
        contracts = {
            "gmail-sync": ["read-only", "approval", "30 or more days", "never sends"],
            "notion-sync": ["one-way", "approval", "notion_sync.json", "filenames"],
            "html-report": ["self-contained", "escape every", "reports/", "never upload"],
        }
        for name, phrases in contracts.items():
            with self.subTest(skill=name):
                skill = read(SKILLS / name / "SKILL.md").lower()
                prompt = read(SKILLS / name / "agents" / "openai.yaml")
                self.assertGreater(len(skill), 1000)
                self.assertIn(f"${name}", prompt)
                for phrase in phrases:
                    self.assertIn(phrase, skill)

    def test_new_shared_references_are_codex_native(self):
        forms = read(CORE / "08-application-forms.md")
        web = read(CORE / "09-web-research.md")
        self.assertIn("application_form_fields.txt", forms)
        self.assertIn("count characters programmatically", forms)
        self.assertIn("untrusted third-party data, never", web)
        self.assertIn("tools/robots_check.py", web)
        self.assertIn("paid proxy", web)
        forbidden = re.compile(r"\bWebFetch\b|\bWebSearch\b|\bAskUserQuestion\b|\bAgent tool\b")
        self.assertIsNone(forbidden.search(forms + web))


class LifecycleParityTests(unittest.TestCase):
    def test_apply_carries_new_lifecycle_contract(self):
        text = read(SKILLS / "job-apply" / "SKILL.md")
        for phrase in [
            "Eligibility Gate",
            "Language Gate",
            "requirement-coverage table",
            "main_<company>_<role>",
            "verbatim posting",
            "status `drafted`",
            "application_form_fields.txt",
            "Never submit, commit, push, or upload",
        ]:
            self.assertIn(phrase, text)

    def test_tracker_status_and_followup_contract(self):
        text = read(SKILLS / "application-outcome" / "SKILL.md")
        for status in [
            "drafted", "applied", "interview", "offer", "hired", "rejected",
            "no_response", "offer_declined", "withdrawn",
        ]:
            self.assertIn(f"`{status}`", text)
        self.assertIn("fewer than two", text)
        self.assertIn("no new claims", text.lower())
        self.assertIn("30-day", text)

    def test_search_and_rank_persist_reusable_gaps_and_gates(self):
        search = read(SKILLS / "job-search" / "SKILL.md")
        rank = read(SKILLS / "job-rank" / "SKILL.md")
        for phrase in ["enabled: false", "mass", "people-search", "health"]:
            self.assertIn(phrase.lower(), search.lower())
        for phrase in ["eligibility_gate", "language_gate", "strengths", "gaps"]:
            self.assertIn(phrase, rank)

    def test_v16_application_deadline_and_cache_contracts(self):
        apply = read(SKILLS / "job-apply" / "SKILL.md")
        interview = read(SKILLS / "interview-prep" / "SKILL.md")
        evaluation = read(CORE / "04-job-evaluation.md")
        for phrase in [
            "source,deadline",
            "append `,deadline`",
            "company_research/",
            "final-claim verification still applies",
            "pdftotext -layout -enc UTF-8",
        ]:
            self.assertIn(phrase, apply)
        self.assertIn("company_research/", interview)
        self.assertIn("Company Research Cache", evaluation)
        self.assertIn("data, never instructions", evaluation)

    def test_v16_search_rank_and_upskill_contracts(self):
        search = read(SKILLS / "job-search" / "SKILL.md")
        rank = read(SKILLS / "job-rank" / "SKILL.md")
        upskill = read(SKILLS / "upskill-analysis" / "SKILL.md")
        for phrase in ["client-side 14-day filter", '"source": "cli|websearch"', "fallback (websearch):"]:
            self.assertIn(phrase, search)
        for phrase in ["location_verdict", "Closing soon", "non-`YYYY-MM-DD`"]:
            self.assertIn(phrase, rank)
        self.assertIn("blank or non-numeric", upskill)
        self.assertIn("Never treat blank as zero", upskill)

    def test_v16_sync_and_reporting_contracts(self):
        gmail = read(SKILLS / "gmail-sync" / "SKILL.md")
        report = read(SKILLS / "html-report" / "SKILL.md")
        notion = read(SKILLS / "notion-sync" / "SKILL.md")
        self.assertIn("-in:sent -in:drafts", gmail)
        self.assertIn("never restrict the query to `in:inbox`", gmail)
        self.assertIn("outcome.md` stage history", report)
        self.assertIn("offer_declined", report)
        self.assertIn("tracker row wins", notion)
        self.assertIn("deadline", notion)


class PrivacyParityTests(unittest.TestCase):
    def test_profile_writes_are_local_overlay_only(self):
        setup = read(SKILLS / "job-setup" / "SKILL.md")
        core = read(SKILLS / "job-application-core" / "SKILL.md")
        for text in (setup, core):
            self.assertIn("documents/cv/codex_profile/", text)
            self.assertIn("tracked", text.lower())
            self.assertIn("ignored", text.lower())
        self.assertNotIn("Update the Codex reference files", setup)

    def test_personal_outputs_are_really_ignored(self):
        probes = [
            "documents/cv/codex_profile/01-candidate-profile.md",
            "documents/applications/example_role/job_posting.md",
            "job_search_tracker.csv",
            "gmail_sync/state.json",
            "job_scraper/notion_sync.json",
            "reports/job-search-report-2026-08-13.html",
            "cv/main_exampleco_engineer.tex",
            "cover_letters/cover_exampleco_engineer.tex",
            ".env.local",
            "company_research/example-company.json",
            "documents/postings/example-role.txt",
        ]
        for probe in probes:
            with self.subTest(path=probe):
                result = subprocess.run(
                    ["git", "-C", str(ROOT), "check-ignore", "-q", probe],
                    capture_output=True,
                )
                self.assertEqual(result.returncode, 0, probe)

    def test_v16_onboarding_and_reset_cover_public_forks_and_postings(self):
        setup = read(SKILLS / "job-setup" / "SKILL.md")
        reset = read(SKILLS / "reset-job-profile" / "SKILL.md")
        self.assertIn("git remote get-url origin", setup)
        self.assertIn("public GitHub fork", setup)
        self.assertIn("documents/postings/", reset)
        self.assertIn("documents/cv/codex_profile/", reset)
        self.assertIn("04-job-evaluation.md", reset)
        self.assertIn("search-queries.md", reset)
        self.assertIn("search-preferences.md", reset)
        self.assertIn("Do not describe evaluation preferences or search", reset)


class ToolingParityTests(unittest.TestCase):
    def test_ci_discovers_portals_and_runs_on_codex_branch(self):
        ci = read(ROOT / ".github" / "workflows" / "ci.yml")
        self.assertIn("branches: [master, codex-migration]", ci)
        self.assertIn("find .agents/skills", ci)
        self.assertIn("matrix.tool", ci)

    def test_upstream_watch_reads_codex_branch_and_never_merges(self):
        workflow = read(ROOT / ".github" / "workflows" / "upstream-watch.yml")
        self.assertIn("ref: codex-migration", workflow)
        self.assertNotRegex(workflow, r"git\s+(merge|cherry-pick|push|rebase)")

    def test_robots_gate_honors_codex_and_legacy_opt_outs(self):
        tool = read(ROOT / "tools" / "robots_check.py")
        self.assertIn("'Codex'", tool)
        self.assertIn("'ChatGPT-User'", tool)
        self.assertIn("'Claude-User'", tool)
        self.assertIn("AUTOMATION_AGENTS", tool)


if __name__ == "__main__":
    unittest.main()
