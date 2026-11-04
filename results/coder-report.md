# Coder Agent Report 
 
## Change 
Change ID: CR-01
Branch: ada09/cr-01
Base commit: c4dca4d7bdb6a794833915c95f4aeec484d0b3c5
 
## Requirements Covered - FR-__ - AC-__ 
- FR-01: The system shall allow users to search customers by name, surname, full name, or email address.
- FR-02: The system shall accept partial matches and display customers whose name, surname, or email address contains the search string entered by the user.
- AC-01: Search by customer name returns matching customer.
- AC-02: Search by email address returns matching customer.
- AC-03: Substring search across searchable fields returns matching customers.
 
## Implementation Plan 
1. Review CHANGE_REQUEST.md, AGENTS.md, SPEC.md, and ARCHITECTURE.md to confirm change scope, contracts, and constraints.
2. Implement optional `field` filter parameter on `SearchService` operations (`search()`, `find_matches()`, and `execute_search()`) and top-level convenience functions (`search()`, `execute_search()`).
3. Restrict matching to valid customer fields (`VALID_SEARCH_FIELDS = frozenset({"name", "surname", "full_name", "email"})`) in `classify_match()` and raise `ValueError` for unsupported field names across search operations. Preserve default behavior across all fields when `field` is omitted or `None`.
4. Ensure public symbol export parity across `search_service.py`, `search.py` (alias), and `__init__.py`.
5. Add and update automated tests in `tests/test_search_field_filter.py` verifying field filtering (`email`, `name`, `surname`, `full_name`), `find_matches()` classification, default fallback when `field=None`, `ValueError` on invalid field names, and `execute_search()` response models.
6. Execute the full repository verification command (`scripts/verify_repo.ps1`), linting, type-checking, and coverage tests.
 
## Files Changed 
- `src/customer_search/search_service.py`: Added `VALID_SEARCH_FIELDS` constant, added optional `field` parameter to `classify_match()`, `find_matches()`, `get_exact_matches()`, `get_partial_matches()`, `search()`, and `execute_search()` with `ValueError` validation on unsupported field names.
- `src/customer_search/search.py`: Re-exported `VALID_SEARCH_FIELDS` to preserve alias module export parity.
- `src/customer_search/__init__.py`: Re-exported `VALID_SEARCH_FIELDS` at the package root to preserve API parity.
- `tests/test_search_field_filter.py`: Unit tests verifying field-specific filtering, `find_matches()` match types, default behavior, invalid field validation, convenience functions, and SearchResult behavior.
 
## Tests Added / Updated 
- `tests/test_search_field_filter.py::test_filter_by_email_only`: Verifies `field="email"` returns only customers whose email matches the query.
- `tests/test_search_field_filter.py::test_filter_by_name_only`: Verifies `field="name"` returns only customers whose first name matches the query.
- `tests/test_search_field_filter.py::test_filter_by_surname_only`: Verifies `field="surname"` returns only customers whose surname matches the query with exact matches prioritized.
- `tests/test_search_field_filter.py::test_filter_by_full_name_only`: Verifies `field="full_name"` returns only customers whose full name matches the query.
- `tests/test_search_field_filter.py::test_find_matches_with_field_filter`: Verifies `find_matches()` restricts matching to specified field and returns correct `MatchType` (exact vs. partial).
- `tests/test_search_field_filter.py::test_filter_none_or_omitted_preserves_default_behavior`: Verifies omitting `field` or passing `None` preserves evaluation across all searchable attributes without regression.
- `tests/test_search_field_filter.py::test_unsupported_field_raises_value_error`: Verifies providing an unsupported field name raises `ValueError` across `search`, `find_matches`, `execute_search`, and `classify_match`.
- `tests/test_search_field_filter.py::test_execute_search_with_field_filter`: Verifies `execute_search()` respects field filtering, empty query validation, and `SearchResult` message behavior.
- `tests/test_search_field_filter.py::test_convenience_functions_support_field_filter`: Verifies top-level `search()` and `execute_search()` functions support the `field` parameter.
- `tests/test_search_field_filter.py::test_valid_search_fields_constant`: Verifies `VALID_SEARCH_FIELDS` contains exact expected customer attributes.
 
## Commands Executed 
- `git status`: Verified working tree status and branch context.
- `git log -n 5 --oneline`: Checked recent commit history.
- `git diff c4dca4d HEAD --name-status`: Checked changed files against base commit.
- `ruff format tests/test_search_field_filter.py`: Validated code formatting against repository rules.
- `ruff check .`: Ran automated code quality and linting checks.
- `mypy src tests`: Ran static type checker.
- `pytest -v`: Executed the full test suite with verbose reporting.
- `powershell -ExecutionPolicy Bypass -File scripts/verify_repo.ps1`: Executed integrated 6-stage repository verification script.
 
## Verification Result 
- Repository Contract Check (`scripts/check_repo_contract.py`): PASS (`REPO_CONTRACT: PASS`)
- Protected Files Integrity & Read-Only Check: PASS (`data/customers.json`, `REQUIREMENTS.md`, `SPEC.md` intact and non-writable)
- Code Formatting (`ruff format --check .`): PASS (43 files already formatted)
- Linter (`ruff check .`): PASS (All checks passed!)
- Type Checker (`mypy src tests`): PASS (Success: no issues found in 21 source files)
- Test Suite & Coverage (`pytest`): PASS (99 passed in 1.23s, 95.19% total coverage exceeding >= 90% threshold)
- Repository Cleanliness: PASS (No tracked or untracked bytecode or cache artifacts)
- Overall Status: `VERIFY_REPO: PASS`
 
## Assumptions 
- The field filter parameter `field` is case-sensitive and must be one of `"name"`, `"surname"`, `"full_name"`, or `"email"`. Any other string raises a `ValueError`.
- When `field` is omitted or passed as `None`, search preserves default behavior of evaluating across all searchable attributes.
- The command-line interface (`cli.py`) remains bound to the single search field per SR-01, while programmatic callers (services/APIs) utilize the optional `field` filter.
 
## Known Limitations 
- Search filtering is restricted to the four supported attributes defined in `VALID_SEARCH_FIELDS`.
- Result ordering and truncation to a maximum of 10 customers (`MAX_RESULTS = 10`) apply per FR-06 without pagination.
- Dataset `data/customers.json` is strictly read-only and customer records cannot be modified, created, or deleted.
 
## Self-Check 
[x] Scope respected 
[x] Existing tests not weakened 
[x] No undocumented dependency/API introduced 
[x] Ready for independent review 
 
This report is NOT an approval. 
