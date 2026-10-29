# Repository Map

A developer and agent guide to locating code, tests, documentation, and understanding where changes belong in the repository.

## Entry Points

The application is a lightweight Python command-line utility with no database, web server, or external API dependencies. Its entry points and core modules are:

- `src/customer_search/cli.py` — Application CLI entry point. Implements interactive search loop (`input()`) and argument-mode execution (`python src/customer_search/cli.py [query]`), as well as result display formatting.
- `src/customer_search/__main__.py` — Package executable entry point. Delegates to `cli.main()` when executed via `python -m customer_search`.
- `src/customer_search/__init__.py` — Public package root exports and public API definition.
- `src/customer_search/customer.py` — Domain model defining the `Customer` dataclass and derived `full_name` property (`models.py` acts as backward-compatibility alias).
- `src/customer_search/search_service.py` — Core search matching, exact/partial classification, priority ordering, alphabetical tie-breaking, and result-limiting engine (`search.py` acts as backward-compatibility alias).
- `src/customer_search/data_loader.py` — Persistence/data loading layer. Reads and validates customer records from local JSON (`loader.py` acts as backward-compatibility alias).

## Tests

Automated tests are written with `pytest` and reside directly under `tests/`:

- `tests/test_customer.py` — Unit tests for the `Customer` domain model, immutability, and derived full-name formatting.
- `tests/test_data_loader.py` — Unit tests for JSON data loading, record schema validation, corrupted/missing file handling, and large-dataset performance.
- `tests/test_search_matching.py` — Unit tests for query matching across fields (name, surname, full name, email), partial matching, and case insensitivity.
- `tests/test_ordering_and_limit.py` — Unit tests for exact-over-partial ranking, alphabetical sorting tie-breakers, and 10-result limit enforcement.
- `tests/test_validation_and_errors.py` — Unit tests for empty and whitespace-only query validation, error messages, and error handling.
- `tests/test_cli.py` — Unit and integration tests for CLI interaction, argument parsing, prompt formatting, and EOF handling.
- `tests/test_search_field_filter.py` — Unit tests for field-specific search filtering capability (`filter_field`).
- `tests/test_setup.py` — Environment verification tests (Python version compatibility).
- `tests/test_scenarios.py` — End-to-end acceptance tests mapping directly to specification scenarios `TS-01` through `TS-13` and criteria `AC-01` through `AC-11`.

## Change Guide

When modifying features, behavior, or fixing issues, follow this workflow:

1. **Consult Authoritative Documentation First**:
   - Check `TASKS.md` or `TASK_UNDER_TEST.md` for task scope and sequencing.
   - Check `REQUIREMENTS.md` for functional (`FR-xx`) and non-functional (`NFR-xx`) requirements.
   - Check `SPEC.md` for search rules (`SR-xx`), validation rules (`VR-xx`), error handling (`EH-xx`), and acceptance criteria (`AC-xx`).
   - Check `ARCHITECTURE.md` for architectural boundaries, component responsibilities, and data flow.
   - Check `AGENTS.md` and `GEMINI.md` for operational constraints, coding rules, and definitions of done.

2. **Locate the Target Layer**:
   - **Domain Model Changes**: Update `src/customer_search/customer.py`. Re-export symbols in `src/customer_search/models.py` and `src/customer_search/__init__.py`.
   - **Search Logic & Ranking**: Update `src/customer_search/search_service.py`. Re-export public symbols in `src/customer_search/search.py` and `src/customer_search/__init__.py`.
   - **Data Ingestion & Validation**: Update `src/customer_search/data_loader.py`. Re-export public symbols in `src/customer_search/loader.py` and `src/customer_search/__init__.py`.
   - **User Interface & Formatting**: Update `src/customer_search/cli.py` (and `src/customer_search/__main__.py` if entry point flags change).
   - **Traceability & Documentation**: Update `docs/traceability.md` and `README.md` if requirements, acceptance criteria, or test mappings change.

3. **Preserve Export Parity**:
   - Always ensure that public symbols added or modified in implementation modules (`customer.py`, `search_service.py`, `data_loader.py`) maintain identical export signatures in their corresponding alias modules (`models.py`, `search.py`, `loader.py`) and `src/customer_search/__init__.py`.

4. **Add or Update Tests**:
   - Add targeted unit tests in the appropriate `tests/test_*.py` file.
   - For end-to-end or scenario-level acceptance changes, update or add tests in `tests/test_scenarios.py`.
   - Never delete, weaken, or bypass existing tests.

5. **Run Validation Commands**:
   - Execute the unified verification script: `powershell -File scripts/verify_repo.ps1` (Windows PowerShell) or `./scripts/verify_repo.sh` (Bash).
   - Direct test execution remains available via `pytest -v`.

## Do Not Edit Directly

The following files and directories must not be edited directly:

- `data/customers.json` — Strictly read-only local customer dataset by specification constraint (`A-01` and `AGENTS.md` Change Rule 3). Must never be modified, overwritten, or reformatted unless explicitly authorized by a dedicated data update task.
- `REQUIREMENTS.md` & `SPEC.md` — Authoritative source-of-truth documents. Must not be altered to accommodate implementation shortcuts or make failing tests pass.
- `__pycache__/` and `*.pyc` — Generated Python bytecode cache. Automatically generated by Python runtimes and test runners.
- `.pytest_cache/` — Generated test runner cache created by `pytest`.
