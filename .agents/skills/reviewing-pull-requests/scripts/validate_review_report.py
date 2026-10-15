"""Deterministic validation script for PR readiness review reports.
Verifies structure, required sections, and critical metadata without subjective judging.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_CHECKS = [
    {
        "name": "Review Context",
        "patterns": [
            r"(?im)^#+\s*Review\s+Context\b",
            r"(?i)\bReview\s+Context\b",
        ],
        "description": "Section 'Review Context'",
    },
    {
        "name": "Requirements / Acceptance Criteria Reviewed",
        "patterns": [
            r"(?im)^#+\s*Requirements\s*/\s*Acceptance\s+Criteria\s+Reviewed\b",
            r"(?i)Requirements\s*/\s*Acceptance\s+Criteria\s+Reviewed",
        ],
        "description": "Section 'Requirements / Acceptance Criteria Reviewed'",
    },
    {
        "name": "Test Evidence",
        "patterns": [
            r"(?im)^#+\s*Test\s+Evidence\b",
            r"(?i)\bTest\s+Evidence\b",
        ],
        "description": "Section 'Test Evidence'",
    },
    {
        "name": "MUST FIX",
        "patterns": [
            r"(?im)^#+\s*MUST\s+FIX\b",
            r"(?im)^MUST\s+FIX\s*(?::)?$",
        ],
        "description": "Section 'MUST FIX'",
    },
    {
        "name": "SHOULD FIX",
        "patterns": [
            r"(?im)^#+\s*SHOULD\s+FIX\b",
            r"(?im)^SHOULD\s+FIX\s*(?::)?$",
        ],
        "description": "Section 'SHOULD FIX'",
    },
    {
        "name": "OPTIONAL",
        "patterns": [
            r"(?im)^#+\s*OPTIONAL\b",
            r"(?im)^OPTIONAL\s*(?::)?$",
        ],
        "description": "Section 'OPTIONAL'",
    },
    {
        "name": "Open Questions",
        "patterns": [
            r"(?im)^#+\s*Open\s+Questions\b",
            r"(?i)\bOpen\s+Questions\b",
        ],
        "description": "Section 'Open Questions'",
    },
    {
        "name": "Final Review Summary",
        "patterns": [
            r"(?im)^#+\s*Final\s+Review\s+Summary\b",
            r"(?i)\bFinal\s+Review\s+Summary\b",
        ],
        "description": "Section 'Final Review Summary'",
    },
    {
        "name": "MUST FIX count",
        "patterns": [
            r"(?i)MUST\s+FIX\s+count\s*:",
        ],
        "description": "Field 'MUST FIX count:'",
    },
    {
        "name": "Human decision required",
        "patterns": [
            r"(?i)Human\s+decision\s+required",
        ],
        "description": "Line 'Human decision required'",
    },
]


def validate_report(report_path: str | Path) -> tuple[bool, list[str]]:
    """Validates a PR readiness review report file against deterministic structural rules.

    Returns:
        tuple[bool, list[str]]: (is_valid, list_of_errors)
    """
    path = Path(report_path)

    if not path.exists():
        return False, [f"File not found: '{report_path}'"]

    if not path.is_file():
        return False, [f"Path is not a regular file: '{report_path}'"]

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as exc:
        return False, [f"Could not read file '{report_path}': {exc}"]

    missing: list[str] = []

    for check in REQUIRED_CHECKS:
        matched = any(
            re.search(pattern, content) for pattern in check["patterns"]
        )
        if not matched:
            missing.append(check["description"])

    if missing:
        return False, missing

    return True, []


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print("ERROR: Missing report file argument.", file=sys.stderr)
        print("Usage: python validate_review_report.py <path_to_report.md>", file=sys.stderr)
        return 1

    report_path = argv[0]
    is_valid, errors = validate_report(report_path)

    if is_valid:
        print("VALID: PR readiness review structure is complete.")
        return 0

    print("INVALID: PR readiness review structure is incomplete.", file=sys.stderr)
    for error in errors:
        print(f"  - {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
