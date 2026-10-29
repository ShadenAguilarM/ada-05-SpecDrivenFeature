#!/usr/bin/env python3
"""Deterministic repository-readiness and contract checker.

Verifies:
1. Essential repository structure and source-of-truth documentation.
2. Standard commands documented in AGENTS.md.
3. Functional requirement references in SPEC.md.
4. Sensitive filenames tracked by Git.
5. Content-level secret scanning across tracked files.
6. Filesystem-level read-only protection of data/customers.json.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from fnmatch import fnmatch
from pathlib import Path

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
    # Build & Configuration & Hygiene
    ".gitignore",
    ".gitattributes",
    "pyproject.toml",
    "requirements-dev.lock",
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
    # Key Tests
    "tests/test_architecture_contracts.py",
    "tests/test_traceability_contract.py",
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

CONTENT_SECRET_PATTERNS = [
    (r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----", "Private cryptographic key block"),
    (r"\bAKIA[0-9A-Z]{16}\b", "AWS Access Key ID"),
    (r"\bghp_[0-9a-zA-Z]{36}\b", "GitHub personal access token"),
    (r"\bgithub_pat_[0-9a-zA-Z_]{82}\b", "GitHub fine-grained access token"),
    (r"\bxox[baprs]-[0-9a-zA-Z]{10,48}\b", "Slack token"),
    (
        r'(?i)\b(?:api[_-]?key|auth[_-]?token|bearer)\s*=\s*["\'][A-Za-z0-9_\-]{24,}["\']',
        "Hardcoded API or Auth Token",
    ),
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


def check_content_secrets(root: Path) -> list[str]:
    """Scan tracked text files for hardcoded secrets, tokens, and private keys."""
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
    for rel_path in tracked_files:
        file_path = root / rel_path
        if not file_path.is_file():
            continue
        # Skip binary files, check_repo_contract itself, or git metadata
        if (
            file_path.suffix in (".pyc", ".png", ".jpg", ".ico", ".bin")
            or rel_path == "scripts/check_repo_contract.py"
        ):
            continue
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        for pattern, description in CONTENT_SECRET_PATTERNS:
            if re.search(pattern, content):
                errors.append(f"Potential secret detected ({description}) in {rel_path}")
    return errors


def check_data_customers_filesystem_readonly(root: Path) -> list[str]:
    """Verify data/customers.json has filesystem-level read-only protection."""
    data_file = root / "data" / "customers.json"
    if not data_file.exists():
        return ["data/customers.json does not exist"]

    # Verify write access fails
    try:
        with open(data_file, "a", encoding="utf-8") as f:
            f.write(" ")
        return ["Filesystem write protection failed: data/customers.json was opened in write mode!"]
    except PermissionError:
        return []
    except Exception as e:
        # If open fails for other reasons, verify os.access
        if not os.access(data_file, os.W_OK):
            return []
        return [f"Filesystem write protection verification error: {e}"]


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

    # 5. Content-level secret scan across tracked files
    all_errors.extend(check_content_secrets(ROOT))

    # 6. Filesystem read-only protection on data/customers.json
    all_errors.extend(check_data_customers_filesystem_readonly(ROOT))

    if all_errors:
        print("REPO_CONTRACT: FAIL")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print("REPO_CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
