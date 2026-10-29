# Agent Instructions

Operational contract for AI agents working in this repository.

## Read First

Follow this consultation order based on the task:
1. **Scope & Task Assignment**: Read `TASKS.md` or the specific task definition (e.g. `TASK_UNDER_TEST.md`).
2. **Business & System Requirements**: Read `REQUIREMENTS.md` to understand user stories, functional (FR) and non-functional (NFR) requirements, and constraints.
3. **Detailed Specifications**: Read `SPEC.md` for search rules (SR), validation rules (VR), error handling (EH), and acceptance criteria (AC).
4. **Architecture & Boundaries**: Read `ARCHITECTURE.md` before making design or structural changes to understand component responsibilities and limits.
5. **Code & Test Layout**: Consult the Repository Map section below and `README.md` for execution examples and test breakdowns.

## Sources of Truth

Each document serves as the authoritative source for specific knowledge:
- **`REQUIREMENTS.md`**: Authoritative for business requirements, user stories, constraints (`C-xx`), and assumptions (`A-xx`).
- **`SPEC.md`**: Authoritative for feature behavior, domain models, rule definitions (`SR-xx`, `VR-xx`, `EH-xx`), acceptance criteria (`AC-xx`), and test scenarios (`TS-xx`).
- **`ARCHITECTURE.md`**: Authoritative for component responsibilities, data flow, interfaces, and architectural boundaries.
- **`TASKS.md`**: Authoritative for task sequencing, task scope, and verification checklists.

**Contradiction Resolution**: If requirements, specifications, or architectural constraints conflict, **stop and request human clarification**. Do not modify specifications or requirements to make an implementation pass.

## Repository Map

The repository is structured as follows:
- `src/customer_search/`: Core package implementation.
  - **Implementation modules**: `customer.py` (domain model), `data_loader.py` (JSON loading & validation), `search_service.py` (matching, ordering, limit engine), `cli.py` (CLI interaction).
  - **Alias modules**: `models.py`, `loader.py`, `search.py` (re-export implementation symbols for backward compatibility).
  - **Package exports**: `__init__.py` (public package API) and `__main__.py` (CLI entry point).
- `tests/`: Automated test suite using `pytest`.
  - Unit tests: `test_customer.py`, `test_data_loader.py`, `test_search_matching.py`, `test_ordering_and_limit.py`, `test_validation_and_errors.py`, `test_cli.py`.
  - End-to-end / scenario tests: `test_scenarios.py` (verifies TS-01 through TS-13 and AC-01 through AC-11).
  - Change-specific tests: `test_search_field_filter.py` (CR-01).
- `data/customers.json`: Read-only local customer dataset.
- `docs/`: Supporting documentation (`traceability.md`). Note: Detailed `docs/REPO_MAP.md` is planned.
- `results/`: Experimental evidence, audit reports, and test execution logs.
- `pyproject.toml`: Build configuration and pytest options.

## Standard Commands

Commands verified in the target environment (Windows PowerShell, Python 3.11+):

### Environment & Installation
Install pinned development and testing dependencies:
```powershell
pip install -r requirements-dev.lock
pip install -e .
```

### Static Analysis, Linting & Formatting
Run automated code quality and type checks:
```powershell
ruff check .
ruff format --check .
mypy src tests
```

### Running Tests
Execute the full test suite with coverage measurement (configured in `pyproject.toml`):
```powershell
pytest
```
Execute with verbose test-by-test reporting:
```powershell
pytest -v
```

### Running the Application
Interactive CLI mode:
```powershell
python src/customer_search/cli.py
```
Or as a package module (requires `PYTHONPATH=src` if not installed in editable mode):
```powershell
$env:PYTHONPATH="src"; python -m customer_search
```
Command-line argument mode:
```powershell
python src/customer_search/cli.py "Alice"
```

### Integrated Validation & Guardrails
- **Integrated Repository Validation Script**: `scripts/verify_repo.ps1` (Windows PowerShell) and `scripts/verify_repo.sh` (Bash) are configured. Run the verification script as the primary validation command before declaring a task DONE.
- **Configured Guardrails**: Ruff (linter and formatter), Mypy (type checker), and `pytest-cov` (coverage threshold >= 90%) are fully configured in `pyproject.toml`. Pre-commit hook is provided in `.git/hooks/pre-commit`.

## Change Rules

1. **Keep Changes Strictly Scoped**: Modify only files directly required by the authorized task.
2. **Never Delete, Weaken, or Bypass Tests**: All existing tests must continue to pass without altering their assertions or expectations.
3. **Protected Files & Immutability**:
   - `data/customers.json` is strictly read-only by specification (A-01). **Never modify, overwrite, or reformat this file** unless a task explicitly authorizes it.
   - Do not modify `REQUIREMENTS.md` or `SPEC.md` to accommodate implementation decisions.
4. **Preserve Export Parity & Module Conventions**: When adding or updating public symbols in implementation modules (`search_service.py`, `data_loader.py`, `customer.py`), maintain identical exports in corresponding alias modules (`search.py`, `loader.py`, `models.py`) and `__init__.py`.
5. **No Unjustified Dependencies**: Do not introduce third-party runtime libraries. The application runtime must rely solely on Python standard libraries.
6. **Environment & Line Endings**:
   - Files in this repository use Windows CRLF (`\r\n`) line endings. Use whole-file write tools or CRLF-compatible replacement tools to avoid match failures.
   - In PowerShell, empty arguments (`""`) are stripped by the shell. Test empty input validation using automated pytest fixtures (`input_func`) rather than PowerShell command-line invocation.
7. **Clean Working Tree**:
   - Inspect `git status` before and after changes.
   - Do not commit compiled bytecode (`*.pyc`, `__pycache__/`) or temporary cache files (`.pytest_cache/`).

## Stop Conditions

Stop immediately and request human guidance when:
1. **Contradictions in Specifications**: Relevant conflicts exist between `REQUIREMENTS.md`, `SPEC.md`, and `ARCHITECTURE.md`.
2. **Architectural Boundary Escalation**: A solution requires introducing external databases, paid APIs, network services, or altering component responsibilities outside the task scope.
3. **Sensitive or Destructive Operations**: An action requires deleting files, overwriting `data/customers.json`, or executing destructive git commands (`git reset --hard`, `git clean -fd`).
4. **Unverifiable Preconditions**: Essential tools, Python versions, or test configurations cannot be verified or fail unexpectedly.

Do not stop for minor ambiguities that can be resolved by consulting the existing test suite, specifications, or architecture documentation.

## Definition of Done

A task is complete only when all the following conditions are met:
- **Requirement Satisfaction**: The implementation satisfies the applicable requirements and specification rules without adding unrequested functionality.
- **Verification Evidence**: Relevant unit, integration, and scenario tests have executed and passed.
- **Command Transparency**: Commands executed and any unexecutable or failing commands are explicitly reported with terminal output.
- **No Out-of-Scope Changes**: Only task-relevant files were modified; no unrelated files, bytecode, or cache artifacts were changed.
- **Git Status Verified**: `git status` confirms a clean working tree containing only authorized changes.
- **Documentation Accuracy**: Task documentation or execution reports reflect actual observed behavior without unverified assumptions.
