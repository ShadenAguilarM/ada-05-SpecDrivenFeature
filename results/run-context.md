# Run Context

## Change

Change ID: CR-01

## Repository

Repository: ada-05-SpecDrivenFeature (https://github.com/ShadenAguilarM/ada-05-SpecDrivenFeature.git)
Base branch: ada09/cr_01 (origin/ada09/cr_01)
Working branch: ada09/cr-01

## Git Context

Base commit: c4dca4d7bdb6a794833915c95f4aeec484d0b3c5 (refactor: Remove obsolete AI usage log for ADA-08)
Initial commit: b0d0dd53f5b3e2f82fe7c6940efa54a793f12940 (Repository root commit: Add initial project documentation for Customer Search feature) / Branch creation commit: c4dca4d7bdb6a794833915c95f4aeec484d0b3c5 (no commits yet on working branch ada09/cr-01)
Working tree status: Untracked file `CHANGE_REQUEST.md` present; no modified or staged tracked files (clean working tree).

## Environment

Operating system: Windows 11 Home Single Language (Version 10.0.26100 Build 26100 / Microsoft Windows NT 10.0.26200.0)
Runtime versions: Python 3.14.3, Windows PowerShell 5.1.26100.9711
Relevant tools: pytest 9.1.1 (with pytest-cov 7.1.0), ruff 0.17.3, mypy 2.4.1, git 2.53.0.windows.2, pip 26.2.1

## Initial Verification

Tests: Passed (`pytest` -> 98 passed in 1.28s, total test coverage 95.19% exceeding the >= 90% threshold configured in pyproject.toml).
Lint: Passed (`ruff check .` -> "All checks passed!"; `ruff format --check .` -> "42 files already formatted").
Other checks: Passed (`mypy src tests` -> "Success: no issues found in 21 source files"; `python scripts/check_repo_contract.py` -> "REPO_CONTRACT: PASS"; `scripts/verify_repo.ps1` guardrails validated).

## Notes

Known limitations:
- Read-only data source: Customer records are stored in `data/customers.json` and cannot be modified, created, or deleted via search operations.
- CLI-only interface: No graphical or web UI is supported.
- Result cap & no pagination: Maximum of 10 results returned per search (FR-06); no pagination or page navigation supported.
- Field search boundaries: Default search evaluates name, surname, full name, and email. Empty or whitespace-only inputs are rejected (FR-08).
- PowerShell shell invocation: Empty string arguments (`""`) are dropped by PowerShell command-line parsing, requiring empty-input validation to be tested via pytest fixtures.
- Line ending sensitivity: Repository files use Windows CRLF (`\r\n`), requiring exact line-ending awareness when inspecting or editing files.

Relevant repository constraints:
- C-01: Python 3.11+, CLI, and pytest.
- C-02: Solution must not require a database.
- C-03: No paid APIs or external network services.
- A-01: Customer records loaded from local JSON file (`data/customers.json`).
- Runtime dependency constraint: Application runtime must rely exclusively on Python standard libraries (no third-party runtime dependencies allowed).
- Protected files immutability: `data/customers.json`, `REQUIREMENTS.md`, and `SPEC.md` are strictly read-only and must never be modified or overwritten.
- Strict scope & test preservation: Modify only files authorized by the task; existing tests must never be deleted, bypassed, or weakened.
- Export parity: Symbols exported by implementation modules (`search_service.py`, `data_loader.py`, `customer.py`) must remain identical in alias modules (`search.py`, `loader.py`, `models.py`) and `__init__.py`.
- Clean working tree: Do not commit compiled bytecode (`*.pyc`, `__pycache__/`) or temporary test cache directories.
- Coverage requirement: Test coverage must meet or exceed 90%.
