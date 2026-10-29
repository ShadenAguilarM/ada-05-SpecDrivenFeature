"""Automated Requirements-to-Tests Traceability Contract Verification.

Satisfies: OBS-06 / Dimension: Requirements & Traceability.
Verifies:
1. docs/traceability.md exists and is structurally valid.
2. All requirements (FR-01 through FR-08, NFR-01 through NFR-03) are mapped.
3. All referenced implementation and test files exist on disk.
4. All referenced test scenarios (TS-01 through TS-13) exist in tests/test_scenarios.py.
5. All acceptance criteria (AC-01 through AC-11) have corresponding test coverage.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_REQUIREMENTS = [
    "FR-01",
    "FR-02",
    "FR-03",
    "FR-04",
    "FR-05",
    "FR-06",
    "FR-07",
    "FR-08",
    "NFR-01",
    "NFR-02",
    "NFR-03",
]

REQUIRED_ACS = [
    "AC-01",
    "AC-02",
    "AC-03",
    "AC-04",
    "AC-05",
    "AC-06",
    "AC-07",
    "AC-08",
    "AC-09",
    "AC-10",
    "AC-11",
]

REQUIRED_SCENARIOS = [
    "TS-01",
    "TS-02",
    "TS-03",
    "TS-04",
    "TS-05",
    "TS-06",
    "TS-07",
    "TS-08",
    "TS-09",
    "TS-10",
    "TS-11",
    "TS-12",
    "TS-13",
]


def test_traceability_matrix_file_exists():
    """Verify docs/traceability.md exists and is non-empty."""
    trace_path = ROOT / "docs" / "traceability.md"
    assert trace_path.is_file(), "docs/traceability.md must exist"
    assert len(trace_path.read_text(encoding="utf-8").strip()) > 100


def test_traceability_matrix_covers_all_requirements():
    """Verify all FR and NFR requirements are present in docs/traceability.md."""
    content = (ROOT / "docs" / "traceability.md").read_text(encoding="utf-8")
    for req in REQUIRED_REQUIREMENTS:
        assert req in content, f"Missing requirement '{req}' in docs/traceability.md"


def test_traceability_matrix_referenced_files_exist():
    """Verify every implementation and test file mentioned in the matrix exists on disk."""
    content = (ROOT / "docs" / "traceability.md").read_text(encoding="utf-8")
    # Extract all backtick-wrapped paths like `src/...` or `tests/...`
    file_refs = re.findall(r"`((?:src|tests)/[^`]+)`", content)
    assert len(file_refs) > 0, "No file references extracted from traceability matrix"
    for file_ref in file_refs:
        full_path = ROOT / file_ref
        assert full_path.exists(), f"Traceability references non-existent file: {file_ref}"


def test_traceability_matrix_test_scenarios_exist_in_test_scenarios_py():
    """Verify TS-01 through TS-13 have matching executable test functions in tests/test_scenarios.py."""
    scenarios_py = ROOT / "tests" / "test_scenarios.py"
    assert scenarios_py.is_file(), "tests/test_scenarios.py must exist"
    content = scenarios_py.read_text(encoding="utf-8")

    for scenario_id in REQUIRED_SCENARIOS:
        func_prefix = f"test_{scenario_id.lower().replace('-', '_')}"
        assert func_prefix in content, (
            f"Scenario '{scenario_id}' missing matching test function '{func_prefix}' in test_scenarios.py"
        )


def test_traceability_matrix_acceptance_criteria_coverage():
    """Verify all acceptance criteria AC-01 through AC-11 are represented in the matrix."""
    content = (ROOT / "docs" / "traceability.md").read_text(encoding="utf-8")
    for ac in REQUIRED_ACS:
        assert ac in content, f"Missing acceptance criteria '{ac}' in docs/traceability.md"
