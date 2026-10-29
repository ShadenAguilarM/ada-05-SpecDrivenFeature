## **Changes Made**

### Improvement I-01

- **Category:** Guardrail
- **Related Finding:** IK-06 / Audit Dimension: Automation & Guardrails, Safety & Permissions
- **Problem:** Absence of `.gitignore` causes Python bytecode (`__pycache__/*.pyc`) and test cache metadata (`.pytest_cache/`) to be tracked and modified during test runs, creating noisy diffs and risk of committing binary artifacts.
- **Target File:** `.gitignore` (new file)
- **Change:** Add a standard Python `.gitignore` covering `__pycache__/`, `*.pyc`, `*.pyo`, `.pytest_cache/`, `.coverage`, `dist/`, `build/`, and `.venv/`. Untrack previously committed bytecode via `git rm -r --cached __pycache__`.
- **Evidence:** `Test-Path .gitignore` returned `False`; `git ls-files "*pycache*"` returned 25 tracked `.pyc` files; `git status` repeatedly reported modified binary `.pyc` files during the BEFORE run.
- **Verification:** Run `pytest`, then verify with `git status` that working tree remains clean without unstaged binary diffs.
- **Priority:** High

---

### Improvement I-02

- **Category:** Context / Guardrail
- **Related Finding:** IK-01, IK-02, IK-04 / Audit Dimension: Agent Instructions, Safety & Permissions
- **Problem:** `AGENTS.md` defines general high-level rules (30 lines) but lacks actionable terminal recipes, fails to list protected/immutable files (such as `data/customers.json`), and provides no operational guidance for Windows CRLF line endings or PowerShell argument parsing.
- **Target File:** `AGENTS.md` (modify)
- **Change:** Expand `AGENTS.md` with:
  1. `Standard Commands`: Exact reproducible commands for running tests (`pytest`, `pytest -v`), running CLI in interactive and argument modes, and running repo verification.
  2. `Protected Files & Boundaries`: Explicit negative constraints listing files that must never be edited by agents (`data/customers.json`, `REQUIREMENTS.md`, `SPEC.md`).
  3. `Environment & Shell Notes`: Instructions regarding Windows CRLF line endings (requiring whole-file write or CRLF-compatible replacement) and PowerShell argument conventions (using pytest fixtures rather than direct PowerShell empty strings).
- **Evidence:** `edit_file` failure in `results/before-agent-run.md`; PowerShell argument stripping in `results/agent-report.md` (Problem 3); lack of explicit `data/` protection in `AGENTS.md`.
- **Verification:** Review `AGENTS.md` against project constraints to ensure instructions are concrete, non-contradictory, and verifiable.
- **Priority:** High

---

### Improvement I-03

- **Category:** Executable Knowledge / Guardrail
- **Related Finding:** IK-03, IK-04, IK-06 / Audit Dimension: Build / Run / Test, Automation & Guardrails
- **Problem:** There is no single, deterministic command to validate repository integrity (running tests, ensuring protected files remain unmodified, and verifying no unwanted files are staged).
- **Target File:** `scripts/verify_repo.ps1` (new file)
- **Change:** Implement a lightweight PowerShell verification script that:
  1. Confirms the SHA-256 hash of `data/customers.json` matches baseline.
  2. Sets `PYTHONPATH=src` and executes the full pytest test suite (`pytest -v`).
  3. Checks `git status --porcelain` to verify no untracked `.pyc` or unauthorized modified files exist.
  4. Returns exit code 0 on success and non-zero on failure.
- **Evidence:** Audit Dimension: Build / Run / Test (Score 4/5) and Automation & Guardrails (Score 1/5) noted absence of a unified task runner.
- **Verification:** Run `powershell -File scripts/verify_repo.ps1` on clean working copy (expect exit code 0); simulate failure (expect non-zero exit code).
- **Priority:** High

---

### Improvement I-04

- **Category:** Navigation
- **Related Finding:** IK-05 / Audit Dimension: Entry Point & Navigation, Architecture Boundaries
- **Problem:** An agent inspecting the codebase must infer the relationship between implementation modules (`search_service.py`, `data_loader.py`, `customer.py`) and alias modules (`search.py`, `loader.py`, `models.py`), as well as the precedence between documentation artifacts.
- **Target File:** `docs/REPO_MAP.md` (new file)
- **Change:** Create a concise repository map providing:
  1. Component mapping: Clear distinction between core implementation modules, backward-compatibility alias modules, and package root exports (`__init__.py`).
  2. Test mapping: Table connecting each source module to its corresponding test file in `tests/`.
  3. Document hierarchy: Authoritative order of truth (`REQUIREMENTS.md` > `SPEC.md` > `ARCHITECTURE.md` > `TASKS.md`).
- **Evidence:** Multi-module modifications were required during `CR-01` implementation in BEFORE run; `docs/traceability.md` is static and does not document module layout.
- **Verification:** Verify that all files in `src/` and `tests/` are accurately documented with clear modification guidelines.
- **Priority:** Medium

---

### Improvement I-05

- **Category:** Guardrail
- **Related Finding:** IK-01 / Audit Dimension: Automation & Guardrails, Entry Point & Navigation
- **Problem:** Inconsistent line-ending handling across developer environments and agent tools leads to string replacement mismatch errors.
- **Target File:** `.gitattributes` (new file)
- **Change:** Add a `.gitattributes` file configuring automated text normalization for repository files (e.g. `* text=auto eol=lf` or consistent checkout policies) and preventing binary interpretation of test JSON fixtures.
- **Evidence:** `edit_file` failed in `results/before-agent-run.md` due to CRLF line endings.
- **Verification:** Verify with `git check-attr -a src/customer_search/search_service.py` that line ending attributes are recognized.
- **Priority:** Medium

---

### Improvement I-06

- **Category:** Test / Guardrail
- **Related Finding:** IK-05 / Audit Dimension: Architecture Boundaries, Testability & Evidence
- **Problem:** Re-export parity between implementation modules and alias modules is currently maintained manually, creating a risk that new functions or constants added to `search_service.py` are omitted from `search.py` or `__init__.py`.
- **Target File:** `tests/test_architecture_contracts.py` (new file)
- **Change:** Add an automated unit test verifying that:
  1. All public symbols in `customer_search.search_service.__all__` are present in `customer_search.search.__all__` and `customer_search.__all__`.
  2. Public exports from `data_loader.py` and `customer.py` are matched in `loader.py` and `models.py`.
- **Evidence:** During `CR-01`, `VALID_SEARCH_FIELDS` had to be manually added to three separate files without automated contract verification.
- **Verification:** Run `pytest tests/test_architecture_contracts.py` and verify that intentional omission of an export triggers a test failure.
- **Priority:** Low

---

### Improvement I-07

- **Category:** CI Check
- **Related Finding:** Audit Dimension: Automation & Guardrails (Score 1/5)
- **Problem:** There is no automated continuous integration workflow validating pull requests or commits in a pristine virtual environment.
- **Target File:** `.github/workflows/ci.yml` (new file)
- **Change:** Create a minimal, fast GitHub Actions workflow that:
  1. Checks out the repository.
  2. Sets up Python 3.11 and 3.12.
  3. Installs `pytest`.
  4. Runs the test suite via `pytest -v`.
- **Evidence:** `Test-Path .github` returned `False`; Audit Dimension 6 scored 1/5 due to complete lack of CI.
- **Verification:** Validate workflow syntax with GitHub Actions schema or actionlint.
- **Priority:** Low