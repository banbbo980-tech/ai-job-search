#!/usr/bin/env python3
"""Codex migration compatibility checks.

Run from anywhere:

    python tools/codex_compatibility.py

The legacy Claude files are intentionally retained during migration. These
checks focus on active Codex surfaces: AGENTS.md and the new workflow skills.
"""

from __future__ import annotations

import re
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("codex_compatibility.py requires PyYAML: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_WORKFLOW_SKILLS = [
    "job-application-core",
    "job-setup",
    "job-search",
    "job-rank",
    "job-apply",
    "profile-expand",
    "interview-prep",
    "application-outcome",
    "upskill-analysis",
    "add-document-template",
    "add-job-portal",
    "reset-job-profile",
    "sync-upstream",
]

CORE_REFERENCES = [
    "01-candidate-profile.md",
    "02-behavioral-profile.md",
    "03-writing-style.md",
    "04-job-evaluation.md",
    "05-cv-templates.md",
    "06-cover-letter-templates.md",
    "07-interview-prep.md",
    "search-queries.md",
]

FORBIDDEN_ACTIVE_PATTERNS = [
    (re.compile(r"\bnpm\s+install\s+-g\s+@anthropic-ai/claude-code\b", re.I), "Claude Code global install"),
    (re.compile(r"\banthropic\s+api\s+key\b", re.I), "Anthropic API key requirement"),
    (re.compile(r"\brun\s+claude\b", re.I), "claude executable requirement"),
    (re.compile(r"\bclaude\s+code\s+is\s+required\b", re.I), "Claude Code requirement"),
    (re.compile(r"\bWebFetch\b|\bWebSearch\b|\bAskUserQuestion\b|\bRead tool\b|\bWrite tool\b|\bEdit tool\b|\bAgent tool\b"), "Claude-specific tool name"),
]

REQUIRED_IGNORE_RULES = [
    "salary_data.json",
    "job_scraper/seen_jobs.json",
    "cv/main_*.tex",
    "!cv/main_example.tex",
    "cover_letters/cover_*.tex",
    "documents/cv/**",
    "documents/linkedin/**",
    "documents/diplomas/**",
    "documents/references/**",
    "documents/applications/**",
    "job_search_tracker.csv",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    text = read_text(path)
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("unterminated YAML frontmatter")
    data = yaml.safe_load(text[4:end])
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a mapping")
    return data, text[end + 4 :]


def check_agents(errors: list[str]) -> None:
    path = ROOT / "AGENTS.md"
    if not path.is_file():
        errors.append("AGENTS.md is missing")
        return
    text = read_text(path)
    for phrase in [
        "Project",
        "$job-setup",
        "$job-search",
        "$job-rank",
        "$job-apply",
        "$interview-prep",
        "$application-outcome",
        "$upskill-analysis",
        "$reset-job-profile",
        "$sync-upstream",
        "Never invent",
        "Urdu",
        "pdftotext",
        "lualatex",
        "xelatex",
        "Subagent Review",
    ]:
        if phrase not in text:
            errors.append(f"AGENTS.md: missing required guidance phrase {phrase!r}")


def check_upstream_sync_surface(errors: list[str]) -> None:
    docs = [
        "docs/UPSTREAM_SYNC_POLICY.md",
        "docs/UPSTREAM_UPDATE_GUIDE.md",
        "docs/CODEX_PRODUCTION_CHECKLIST.md",
        "docs/upstream-state.json",
        "tools/check_upstream_updates.py",
    ]
    for relpath in docs:
        path = ROOT / relpath
        if not path.is_file():
            errors.append(f"{relpath} is missing")

    state_path = ROOT / "docs" / "upstream-state.json"
    if state_path.is_file():
        try:
            state = json.loads(read_text(state_path))
        except json.JSONDecodeError as exc:
            errors.append(f"docs/upstream-state.json: invalid JSON: {exc}")
        else:
            required = {
                "schema_version",
                "official_repository_url",
                "last_integrated_upstream_commit",
                "integration_date",
                "codex_branch",
                "parity_test_status",
                "migration_report_path",
            }
            missing = required - set(state)
            if missing:
                errors.append(f"docs/upstream-state.json: missing fields {sorted(missing)}")
            if state.get("official_repository_url") != "https://github.com/MadsLorentzen/ai-job-search":
                errors.append("docs/upstream-state.json: official_repository_url is incorrect")
            if not re.match(r"^[0-9a-f]{40}$", str(state.get("last_integrated_upstream_commit", "")), re.I):
                errors.append("docs/upstream-state.json: last_integrated_upstream_commit must be a full hash")
            if state.get("codex_branch") != "codex-migration":
                errors.append("docs/upstream-state.json: codex_branch must be codex-migration")


def check_skills(errors: list[str]) -> None:
    names: dict[str, Path] = {}
    descriptions: dict[str, Path] = {}

    for skill in REQUIRED_WORKFLOW_SKILLS:
        skill_dir = ROOT / ".agents" / "skills" / skill
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{rel(skill_file)} is missing")
            continue
        try:
            data, body = parse_frontmatter(skill_file)
        except ValueError as exc:
            errors.append(f"{rel(skill_file)}: {exc}")
            continue
        name = data.get("name")
        description = data.get("description")
        if name != skill:
            errors.append(f"{rel(skill_file)}: expected name {skill!r}, got {name!r}")
        if not isinstance(description, str) or len(description.strip()) < 40:
            errors.append(f"{rel(skill_file)}: description is missing or too short")
        if "TODO" in body or "TODO" in str(description):
            errors.append(f"{rel(skill_file)}: contains TODO placeholder")
        if name in names:
            errors.append(f"{rel(skill_file)}: duplicate skill name also in {rel(names[name])}")
        names[name] = skill_file
        if description in descriptions:
            errors.append(
                f"{rel(skill_file)}: duplicate skill description also in {rel(descriptions[description])}"
            )
        descriptions[description] = skill_file
        for pattern, label in FORBIDDEN_ACTIVE_PATTERNS:
            if pattern.search(read_text(skill_file)):
                errors.append(f"{rel(skill_file)}: active workflow contains {label}")

        openai_yaml = skill_dir / "agents" / "openai.yaml"
        if not openai_yaml.is_file():
            errors.append(f"{rel(openai_yaml)} is missing")
        elif f"${skill}" not in read_text(openai_yaml):
            errors.append(f"{rel(openai_yaml)}: default prompt must mention ${skill}")


def check_core_references(errors: list[str]) -> None:
    ref_dir = ROOT / ".agents" / "skills" / "job-application-core" / "references"
    for filename in CORE_REFERENCES:
        path = ref_dir / filename
        if not path.is_file():
            errors.append(f"{rel(path)} is missing")
    if not errors:
        refs_text = "\n".join(read_text(ref_dir / name) for name in CORE_REFERENCES)
        for pattern, label in FORBIDDEN_ACTIVE_PATTERNS:
            if pattern.search(refs_text):
                errors.append(f"{rel(ref_dir)}: shared references contain {label}")


def check_workflow_contracts(errors: list[str]) -> None:
    job_apply = read_text(ROOT / ".agents" / "skills" / "job-apply" / "SKILL.md")
    required_apply_phrases = [
        "Codex is the drafter",
        "Should I proceed with drafting",
        "Independent Reviewer",
        "subagents are unavailable",
        "lualatex",
        "xelatex",
        "pdftotext",
        "missing (gap)",
    ]
    for phrase in required_apply_phrases:
        if phrase not in job_apply:
            errors.append(f"job-apply skill: missing workflow contract {phrase!r}")

    reset = read_text(ROOT / ".agents" / "skills" / "reset-job-profile" / "SKILL.md")
    if "exact confirmation text `RESET`" not in reset or "response is exactly `RESET`" not in reset:
        errors.append("reset-job-profile skill: exact RESET confirmation gate is missing")

    job_search = read_text(ROOT / ".agents" / "skills" / "job-search" / "SKILL.md")
    if "Discover portal skills" not in job_search or "Do not guess flags" not in job_search:
        errors.append("job-search skill: portal discovery contract is missing")

    add_template = read_text(ROOT / ".agents" / "skills" / "add-document-template" / "SKILL.md")
    required_add_template_phrases = [
        "Switch Mode",
        "parent folder name exactly",
        "If more than one manifest matches",
        "Verify `template.tex` exists",
        "Do not re-run registration",
        "`--use default` removes the managed block",
        "Exactly one managed block",
        "If activation was reached from Switch Mode",
        "_compile_test.fls",
        "_compile_test.fdb_latexmk",
        "_compile_test.synctex.gz",
        "_compile_test.*",
    ]
    for phrase in required_add_template_phrases:
        if phrase not in add_template:
            errors.append(f"add-document-template skill: missing upstream parity contract {phrase!r}")


def check_gitignore(errors: list[str]) -> None:
    rules = {line.strip() for line in read_text(ROOT / ".gitignore").splitlines()}
    for rule in REQUIRED_IGNORE_RULES:
        if rule not in rules:
            errors.append(f".gitignore: required personal-data rule missing: {rule}")


def main() -> int:
    errors: list[str] = []
    check_agents(errors)
    check_upstream_sync_surface(errors)
    check_skills(errors)
    check_core_references(errors)
    check_workflow_contracts(errors)
    check_gitignore(errors)

    if errors:
        print(f"codex_compatibility: {len(errors)} failure(s)")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        "codex_compatibility: OK "
        f"({len(REQUIRED_WORKFLOW_SKILLS)} workflow skills, "
        f"{len(CORE_REFERENCES)} shared references, AGENTS.md)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
