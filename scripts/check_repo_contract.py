#!/usr/bin/env python3
"""Deterministic repository-readiness and contract checker.

Verifies essential repository structure, required documentation,
standard commands, requirement-ID references, and security conventions.
"""

from fnmatch import fnmatch
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent

ESSENTIAL_PATHS = [
    # Core Documentation & Source-of-Truth Contracts
    "AGENTS.md",
    "README.md",
    "REQUIREMENTS.md",
    "SPEC.md",
    "ARCHITECTURE.md",
    "TASKS.md",
    "docs/REPO_MAP.md",
    "docs/traceability.md",
    # Build & Configuration
    "pyproject.toml",
    # Essential Data
    "data/customers.json",
    # Verification & Contract Scripts
    "scripts/verify_repo.sh",
    "scripts/verify_repo.ps1",
    "scripts/check_repo_contract.py",
    # Core Package Modules & Entry Points
    "src/customer_search/__init__.py",
    "src/customer_search/__main__.py",
    "src/customer_search/cli.py",
    "src/customer_search/customer.py",
    "src/customer_search/search_service.py",
    "src/customer_search/data_loader.py",
    # Required Output / Experimental Directory
    "results",
]

REQUIRED_AGENTS_COMMANDS = [
    "scripts/verify_repo.ps1",
    "scripts/verify_repo.sh",
    "pytest",
]

REQUIRED_SPEC_REQUIREMENTS = [
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

PROHIBITED_TRACKED_PATTERNS = [
    ".env",
    ".env.local",
    "*.pem",
    "*.key",
    "*.p12",
    "id_rsa*",
    "id_dsa*",
]


def check_essential_paths(root: Path) -> list[str]:
    errors = []
    for rel_path in ESSENTIAL_PATHS:
        full_path = root / rel_path
        if not full_path.exists():
            errors.append(f"Missing essential path: {rel_path}")
    return errors


def check_agents_commands(root: Path) -> list[str]:
    agents_path = root / "AGENTS.md"
    if not agents_path.is_file():
        return ["AGENTS.md missing; cannot verify standard commands"]
    content = agents_path.read_text(encoding="utf-8")
    errors = []
    for cmd in REQUIRED_AGENTS_COMMANDS:
        if cmd not in content:
            errors.append(f"AGENTS.md missing standard command documentation: '{cmd}'")
    return errors


def check_spec_requirements(root: Path) -> list[str]:
    spec_path = root / "SPEC.md"
    if not spec_path.is_file():
        return ["SPEC.md missing; cannot verify requirement references"]
    content = spec_path.read_text(encoding="utf-8")
    errors = []
    for req in REQUIRED_SPEC_REQUIREMENTS:
        if req not in content:
            errors.append(f"SPEC.md missing requirement reference: '{req}'")
    return errors


def check_sensitive_tracked_files(root: Path) -> list[str]:
    try:
        proc = subprocess.run(
            ["git", "ls-files"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return []

    if proc.returncode != 0:
        return []

    tracked_files = proc.stdout.splitlines()
    errors = []
    for file_path in tracked_files:
        name = Path(file_path).name
        for pattern in PROHIBITED_TRACKED_PATTERNS:
            if fnmatch(name, pattern):
                errors.append(f"Prohibited sensitive file tracked by git: {file_path}")
                break
    return errors


def main() -> int:
    all_errors = []

    # 1. Essential paths
    all_errors.extend(check_essential_paths(ROOT))

    # 2. Standard commands in AGENTS.md
    all_errors.extend(check_agents_commands(ROOT))

    # 3. Requirement references in SPEC.md
    all_errors.extend(check_spec_requirements(ROOT))

    # 4. Sensitive files tracked by Git
    all_errors.extend(check_sensitive_tracked_files(ROOT))

    if all_errors:
        print("REPO_CONTRACT: FAIL")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print("REPO_CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
