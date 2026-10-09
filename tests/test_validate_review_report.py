"""Unit tests for scripts/validate_review_report.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from scripts.validate_review_report import validate_report


SAMPLE_VALID_REPORT = """# PR Readiness Review

## Review Context
PR / Branch: feature/branch
Reviewer Agent: reviewer-agent
Date: 2026-10-08

## Requirements / Acceptance Criteria Reviewed
- FR-01: OK

## Test Evidence
- pytest: 79 passed

## MUST FIX
None

## SHOULD FIX
None

## OPTIONAL
None

## Open Questions
None

## Final Review Summary
MUST FIX count: 0
SHOULD FIX count: 0
OPTIONAL count: 0

Human decision required:
NO
"""


def test_valid_template_file():
    template_path = Path(".agents/skills/reviewing-pull-requests/assets/review_report_template.md")
    if not template_path.exists():
        template_path = Path("assets/review_report_template.md")
    is_valid, errors = validate_report(template_path)
    assert is_valid is True
    assert errors == []


def test_valid_sample_report(tmp_path: Path):
    report_file = tmp_path / "valid_report.md"
    report_file.write_text(SAMPLE_VALID_REPORT, encoding="utf-8")

    is_valid, errors = validate_report(report_file)
    assert is_valid is True
    assert errors == []


def test_missing_file_returns_false():
    missing_path = Path("results/does_not_exist_xyz.md")
    is_valid, errors = validate_report(missing_path)
    assert is_valid is False
    assert any("File not found" in err for err in errors)


def test_missing_sections(tmp_path: Path):
    sections = [
        "## Review Context",
        "## Requirements / Acceptance Criteria Reviewed",
        "## Test Evidence",
        "## MUST FIX",
        "## SHOULD FIX",
        "## OPTIONAL",
        "## Open Questions",
        "## Final Review Summary",
        "MUST FIX count:",
        "Human decision required",
    ]

    for section in sections:
        incomplete_content = SAMPLE_VALID_REPORT.replace(section, "")
        report_file = tmp_path / "incomplete.md"
        report_file.write_text(incomplete_content, encoding="utf-8")

        is_valid, errors = validate_report(report_file)
        assert is_valid is False, f"Report should be invalid without {section}"
        assert len(errors) >= 1


def test_cli_execution_success(tmp_path: Path):
    report_file = tmp_path / "report.md"
    report_file.write_text(SAMPLE_VALID_REPORT, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "scripts/validate_review_report.py", str(report_file)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "VALID: PR readiness review structure is complete." in result.stdout


def test_cli_execution_missing_argument():
    result = subprocess.run(
        [sys.executable, "scripts/validate_review_report.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "ERROR: Missing report file argument." in result.stderr


def test_cli_execution_invalid_file(tmp_path: Path):
    bad_file = tmp_path / "bad.md"
    bad_file.write_text("# Only Header", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "scripts/validate_review_report.py", str(bad_file)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "INVALID: PR readiness review structure is incomplete." in result.stderr


def test_trigger_cases_valid():
    """Verify that trigger test cases in evals/ are complete and well-formed."""
    import json
    trigger_path = Path(".agents/skills/reviewing-pull-requests/evals/trigger_cases.json")
    assert trigger_path.exists()
    data = json.loads(trigger_path.read_text(encoding="utf-8"))
    assert len(data) == 6
    positive = [c for c in data if c["expected_trigger"] is True]
    negative = [c for c in data if c["expected_trigger"] is False]
    assert len(positive) == 3
    assert len(negative) == 3
    for case in data:
        assert "id" in case
        assert "input" in case
        assert isinstance(case["expected_trigger"], bool)


def test_execution_cases_valid():
    """Verify that execution test cases in evals/ are defined with expected artifacts and behaviors."""
    import json
    exec_path = Path(".agents/skills/reviewing-pull-requests/evals/execution_cases.json")
    assert exec_path.exists()
    data = json.loads(exec_path.read_text(encoding="utf-8"))
    assert len(data) >= 3
    has_boundary = any("boundary" in case["id"] for case in data)
    assert has_boundary, "Must include at least one boundary case"
    for case in data:
        assert "id" in case
        assert "input" in case
        assert "expected_artifacts" in case
        assert "results/pr-readiness-review.md" in case["expected_artifacts"]
        assert "expected_behavior" in case
        assert isinstance(case["expected_behavior"], list)
        assert len(case["expected_behavior"]) > 0

