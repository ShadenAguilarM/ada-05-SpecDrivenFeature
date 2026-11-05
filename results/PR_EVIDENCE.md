# PR Evidence

## Change
Change ID: CR-01
PR Branch: ada09/cr-01
Base commit: c4dca4d7bdb6a794833915c95f4aeec484d0b3c5
Final commit: a30266ea5e67934d98fe06980b07693700422b51

## Requirements / Acceptance Criteria
FR-
- FR-01: The system shall allow users to search customers by name, surname, full name, or email address.
- FR-02: The system shall accept partial matches and display customers whose name, surname, or email address contains the search string entered by the user.
AC-
- AC-01: Given there are registered customers in the system, when the user enters a customer's name into the search field, then the system shall display the corresponding customer (Search by customer name).
- AC-02: Given a registered customer exists with a specific email address, when the user enters that email address into the search field, then the system shall display the corresponding customer (Search by email address).
- AC-03: Given there are customers whose names or email addresses contain a specific text string, when the user enters only a substring of that text, then the system shall display customers whose first name, last name, full name, or email address contains that string (Substring search across searchable fields).

## Implementation
Coder report: `results/coder-report.md`
Files changed:
- `src/customer_search/search_service.py`
- `src/customer_search/search.py`
- `src/customer_search/__init__.py`
- `tests/test_search_field_filter.py`
- `CHANGE_REQUEST.md`
- `results/run-context.md`
- `results/coder-report.md`
- `results/verification-report.md`
- `results/pr.diff`
- `results/commits.txt`
- `results/review-contract.md`
- `results/review-report.md`
- `results/human-review-decisions.md`
- `results/re-review-report.md`
- `results/AI_USAGE_LOG.md`
Commits:
- `0bcabf21982dce26934ec71a25220059a612829d`: feat: Add CHANGE_REQUEST and run-context documentation for customer search field filtering
- `b4134e6cb30f7214fad47bf4eff97aeabcbcb69b`: feat: Implement CR-01 optional field filtering in SearchService and add related unit tests
- `9732898748e779ef83cb3b6a546e07a30dd29ea7`: feat: Add verification report for CR-01 with environment checks and results
- `a30266ea5e67934d98fe06980b07693700422b51`: fix: address ADA-09 review findings

## Verification
Verification command: `powershell -ExecutionPolicy Bypass -File scripts/verify_repo.ps1` / `pytest -v`
Final result: PASS (`VERIFY_REPO: PASS`, Overall Gate: PASS)
Tests: PASS (101 passed in 1.17s; total statement coverage 95.45% exceeding >= 90% threshold; 100% statement coverage on `src/customer_search/search_service.py`)
Lint: PASS (`ruff check .` -> All checks passed!; `ruff format --check .` -> 49 files formatted; `mypy src tests` -> Success: no issues found in 21 source files)
Security/repo checks: PASS (`python scripts/check_repo_contract.py` -> `REPO_CONTRACT: PASS`; 0 sensitive tracked files; 0 hardcoded secrets; filesystem read-only permissions on `data/customers.json`, `REQUIREMENTS.md`, and `SPEC.md` intact and verified)

## Independent Review
Review report: `results/review-report.md` (Commit reviewed: `b4134e6cb30f7214fad47bf4eff97aeabcbcb69b`)
MUST FIX found:
- RF-01 (MUST FIX): PR Integrity & Traceability Discrepancy — Discrepancy between Coder Agent report claims (modifications to `src/` and 10 unit tests) and initial PR diff against base commit `c4dca4d` (which initially lacked production changes due to ancestor commits).
SHOULD FIX found:
- RF-02 (SHOULD FIX): Test Coverage / Validation Gap — Omission of `field="full_name"` in `test_find_matches_with_field_filter` and missing assertions for `MatchType` on surname matches.
- RF-03 (SHOULD FIX): Test Coverage / Public API Contract — Absence of direct unit tests exercising `get_exact_matches()` and `get_partial_matches()` with the `field` parameter.
- RF-04 (SHOULD FIX): Test Coverage / Scenario Asymmetry — Asymmetry in field-specific tests (exact-only or partial-only across `name`, `full_name`, `email`).
- RF-05 (SHOULD FIX): Technical Debt / Performance & Design — Redundant static validation of `VALID_SEARCH_FIELDS` inside per-customer O(N) loop and duplicate full-dataset iteration in `search()`.
OPTIONAL found:
- RF-06 (OPTIONAL): Code Quality / Maintainability — Manual `.strip().lower()` calls repeated 8 times in `classify_match()` instead of reusing domain helper `normalize_text()`.
- RF-07 (OPTIONAL): Code Quality / Maintainability — Method parameter `field` shadowed `dataclasses.field` imported at module top.

## Human Decisions
Accepted:
- RF-01 (MUST FIX): ACCEPTED — Required action: clarify target branch, update `results/coder-report.md` and `results/pr.diff` to accurately reflect the true change delta including production code.
- RF-02 (SHOULD FIX): ACCEPTED — Required action: update `tests/test_search_field_filter.py` with `field="full_name"` test cases and explicit assertions for `MatchType.EXACT` and `MatchType.PARTIAL`.
- RF-03 (SHOULD FIX): ACCEPTED — Required action: add direct unit tests for `get_exact_matches()` and `get_partial_matches()` with `field` parameter.
- RF-04 (SHOULD FIX): ACCEPTED — Required action: add test cases covering exact email, partial name, and partial full_name searches.
- RF-05 (SHOULD FIX): ACCEPTED — Required action: refactor `search()` and `classify_match()` to single pass and avoid redundant loop validation.
- RF-06 (OPTIONAL): ACCEPTED — Required action: refactor to reuse `normalize_text()`.
- RF-07 (OPTIONAL): ACCEPTED — Required action: resolve symbol shadowing by importing `from dataclasses import field as dc_field`.
Modified: None
Rejected: None
Deferred: None (Human gate confirmed: `[X] Return to coder-agent`)

## Re-review
Resolved: 7 findings resolved (`RF-01`, `RF-02`, `RF-03`, `RF-04`, `RF-05`, `RF-06`, `RF-07`)
- RF-01: RESOLVED — Production code modifications in `src/customer_search/search_service.py` (+104 line changes) and test suite updates in `tests/test_search_field_filter.py` (+118 line changes) are actively present in `results/pr.diff` against base commit `c4dca4d`. `results/coder-report.md` accurately describes the changes in the Fix Cycle section.
- RF-02: RESOLVED — Explicit `MatchType.EXACT` and `MatchType.PARTIAL` assertions added for surname matches; `field="full_name"` exact and partial matches tested in `tests/test_search_field_filter.py:119-142`.
- RF-03: RESOLVED — Dedicated unit tests `test_get_exact_matches_with_field_filter` and `test_get_partial_matches_with_field_filter` added to `tests/test_search_field_filter.py:145-194`.
- RF-04: RESOLVED — Symmetric exact and partial match coverage verified across all 4 supported fields (`name`, `surname`, `full_name`, `email`) in `tests/test_search_field_filter.py:42-101`.
- RF-05: RESOLVED — `search()` refactored to single-pass iteration via `find_matches()` with in-memory partitioning; static validation and normalization extracted to `_classify_match_normalized()` outside inner loop.
- RF-06: RESOLVED — Domain helper `normalize_text()` reused across `customer_sort_key` and `_classify_match_normalized()` branches.
- RF-07: RESOLVED — Import aliased as `from dataclasses import field as dc_field` in `src/customer_search/search_service.py:15`.
Partially resolved: 0
Not resolved: 0
New MUST FIX: 0 (Reviewer recommendation: `[X] READY FOR HUMAN REVIEW`)

## Traceability
| Requirement / AC | Task / Change | Code | Test | Review Finding |
| :--- | :--- | :--- | :--- | :--- |
| FR-01 | CR-01 / T-04 | `src/customer_search/search_service.py` (`VALID_SEARCH_FIELDS`, `classify_match`, `_classify_match_normalized`, `find_matches`, `search`, `execute_search`) | `tests/test_search_field_filter.py` (`test_filter_by_name_only`, `test_filter_by_surname_only`, `test_filter_by_full_name_only`, `test_filter_by_email_only`, `test_valid_search_fields_constant`) | RF-01, RF-02, RF-04, RF-05, RF-06, RF-07 |
| FR-02 | CR-01 / T-04 | `src/customer_search/search_service.py` (`_classify_match_normalized`: substring containment) | `tests/test_search_field_filter.py` (`test_filter_by_email_only`, `test_filter_by_name_only`, `test_filter_by_surname_only`, `test_filter_by_full_name_only`, `test_get_partial_matches_with_field_filter`) | RF-02, RF-03, RF-04 |
| AC-01 | CR-01 / T-08 | `src/customer_search/search_service.py` (`_classify_match_normalized` branch `if field == "name"`) | `tests/test_search_field_filter.py::test_filter_by_name_only`, `test_get_exact_matches_with_field_filter` | RF-01, RF-04 |
| AC-02 | CR-01 / T-08 | `src/customer_search/search_service.py` (`_classify_match_normalized` branch `elif field == "email"`) | `tests/test_search_field_filter.py::test_filter_by_email_only`, `test_get_exact_matches_with_field_filter` | RF-01, RF-04 |
| AC-03 | CR-01 / T-04 / T-08 | `src/customer_search/search_service.py` (`_classify_match_normalized` default branch, `find_matches`) | `tests/test_search_field_filter.py::test_filter_none_or_omitted_preserves_default_behavior`, `test_find_matches_with_field_filter` | RF-02, RF-04 |
| CR-01 Error Handling & API Parity | CR-01 / T-06 / T-08 | `src/customer_search/search_service.py` (`VALID_SEARCH_FIELDS` validation raising `ValueError`), `src/customer_search/search.py`, `src/customer_search/__init__.py` | `tests/test_search_field_filter.py::test_unsupported_field_raises_value_error`, `test_execute_search_with_field_filter`, `test_convenience_functions_support_field_filter` | RF-01, RF-03, RF-05 |

## Remaining Risks / Technical Debt
- Upstream target branch alignment: Branch `ada09/cr-01` is branched from commit `c4dca4d7bdb6a794833915c95f4aeec484d0b3c5` (branch `origin/ada09/cr_01`), whereas `main` sits at commit `0f6af39` (which lacks preceding ADA-08 commits). The final merge target branch and any potential fast-forward/rebase onto `main` must be determined and executed by the human repository owner.
- Dedicated latency benchmark for 10,000 customers with field filtering: Although RF-05 optimized `search()` to a single pass and pre-normalized queries, and all 101 tests pass (including performance test `test_load_up_to_10000_customers_performance`), there is no dedicated automated performance test specifically measuring query execution time for `search(..., field=...)` under 10,000 customer records against NFR-01 (< 2 seconds).
- CLI integration scope: Field filtering is currently exposed programmatically via `SearchService.search`, `find_matches`, `execute_search`, and top-level module exports; it is not exposed via command-line arguments in `cli.py`, which continues to use a single search field per SR-01.
- Read-only dataset constraint: The customer dataset `data/customers.json` remains strictly immutable per A-01 and cannot be modified by search operations.
- Case-sensitivity of field parameter: The `field` parameter requires exact lowercase strings (`"name"`, `"surname"`, `"full_name"`, `"email"`). Passing capitalized or invalid strings raises `ValueError`.

## Final Human Decision
- [ ] NOT READY
- [X] READY FOR HUMAN MERGE

Approved by: Ashley Aguilar 
Date: 04/11/2026
