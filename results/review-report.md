# Independent Review Report

## Review Context
Change ID: CR-01
Branch / PR: ada09/cr-01
Commit reviewed: b4134e6cb30f7214fad47bf4eff97aeabcbcb69b
Reviewer agent: Independent Reviewer Agent
Model: Gemini 3.8 Flash (High)
Tools / permissions: Read-only inspection (read_file, run_command for read-only git/pytest queries)

## Requirements Reviewed
- FR-01: Search customers by name, surname, full name, or email address.
- FR-02: Accept partial substring matches across customer attributes.
- FR-03: Case-insensitive search comparison and text normalization.
- FR-04: Order exact matches before partial matches; sort ties alphabetically.
- FR-06: Display a maximum of 10 results per search without pagination.
- FR-08: Validate search term input; reject empty or whitespace-only queries.
- AC-01: Search by customer name returns matching customer.
- AC-02: Search by email address returns matching customer.
- AC-03: Substring search across searchable fields returns matching customers.
- AC-06: Display exact matches before partial matches.
- CR-01: Optional field filter parameter (`field`) on SearchService operations (`search`, `find_matches`, `execute_search`, `get_exact_matches`, `get_partial_matches`) allowing callers to restrict matching to `"name"`, `"surname"`, `"full_name"`, or `"email"`; preserve default behavior when omitted or `None`; and raise `ValueError` for unsupported field names.

## Verification Evidence Reviewed
- `CHANGE_REQUEST.md`: Scope definition, acceptance criteria, constraints, and formal authorization for CR-01.
- `AGENTS.md`: Operational contract, sources of truth, change rules, and definition of done.
- `REQUIREMENTS.md`: System requirements (FR-01 through FR-08, NFR-01 through NFR-03, C-01 through C-03, A-01).
- `SPEC.md`: Authoritative specification (SR-01 through SR-11, VR-01 through VR-04, EH-01 through EH-04, AC-01 through AC-11, TS-01 through TS-13).
- `ARCHITECTURE.md`: Component layering, responsibilities, data flow, interface contracts, and dependency rules.
- `results/run-context.md`: Environment setup, baseline commit `c4dca4d7bdb6a794833915c95f4aeec484d0b3c5`, and platform constraints.
- `results/coder-report.md`: Implementation claims, list of reported files changed, tests added, commands executed, and self-checks.
- `results/verification-report.md`: Execution verification report for commit `b4134e6`, reporting 99 passing tests (95.19% coverage), clean ruff linter/formatter, clean mypy type checks, and repository contract validation.
- `results/review-contract.md`: Scope contract, architectural boundaries, and severity classification rules.
- `results/commits.txt`: Commit log for branch `ada09/cr-01` (`9732898`, `b4134e6`, `0bcabf2`).
- `results/pr.diff`: Full patch between base commit `c4dca4d` and commit `b4134e6`.
- Production codebase:
  - `src/customer_search/search_service.py`: Implementation of `VALID_SEARCH_FIELDS`, `classify_match`, `find_matches`, `get_exact_matches`, `get_partial_matches`, `search`, and `execute_search`.
  - `src/customer_search/search.py`: Re-export parity module for search service symbols.
  - `src/customer_search/__init__.py`: Package-level public symbol exports.
  - `src/customer_search/customer.py`: `Customer` immutable dataclass and derived `full_name`.
  - `src/customer_search/data_loader.py`: JSON loading, validation, and read-only protection.
  - `src/customer_search/cli.py`: Command-line interface and formatting logic.
- Test suite:
  - `tests/test_search_field_filter.py`: Unit tests specifically written for CR-01.
  - `tests/test_architecture_contracts.py`: Architectural boundary and export parity contract tests.
  - `tests/test_search_matching.py`: Baseline search matching tests.
  - `tests/test_ordering_and_limit.py`: Priority ordering, alphabetical sorting, and result capping tests.
  - `tests/test_validation_and_errors.py`: Search input validation and error handling tests.
  - `tests/test_cli.py`: Interactive and argument CLI tests.
  - `tests/test_scenarios.py`: End-to-end acceptance scenarios (TS-01 through TS-13).
- Tool executions:
  - `pytest -v`: Executed all 99 automated tests; 100% passed in 1.07s with 95.19% statement coverage.
  - `git diff c4dca4d b4134e6`: Verified actual file delta against base commit.
  - `git log --graph --oneline`: Analyzed commit tree and lineage across branches `main`, `origin/ada09/cr_01`, and `ada09/cr-01`.

## Findings

### RF-01 MUST FIX
Category: PR Integrity & Traceability Discrepancy
Requirement / AC: CR-01 / AGENTS.md Definition of Done (Documentation Accuracy & Scope Verification)
File/Line: `results/coder-report.md`:73-90 vs `results/pr.diff`:1-224
Evidence:
In `results/coder-report.md` (lines 73-77), the Coder Agent states that the branch modified:
- `src/customer_search/search_service.py`
- `src/customer_search/search.py`
- `src/customer_search/__init__.py`
- `tests/test_search_field_filter.py`
and lists 10 unit tests under "Tests Added / Updated" (lines 79-90).
However, inspecting `results/pr.diff` and executing `git diff c4dca4d7bdb6a794833915c95f4aeec484d0b3c5 b4134e6cb30f7214fad47bf4eff97aeabcbcb69b` demonstrates that the actual PR diff against the declared base commit `c4dca4d` contains:
1. `CHANGE_REQUEST.md` (+38 lines)
2. `results/coder-report.md` (+77 lines)
3. `results/run-context.md` (+51 lines)
4. `tests/test_search_field_filter.py` (+22 lines, containing only `test_find_matches_with_field_filter`)
The PR diff contains ZERO modifications to `src/customer_search/search_service.py`, `src/customer_search/search.py`, or `src/customer_search/__init__.py`. In git history, the production code changes and 9 out of the 10 test functions were already committed in ancestor commit `5454747` prior to base commit `c4dca4d`.
Problem: The PR candidate diff (`results/pr.diff`) does not contain the production code changes required to implement CR-01. The coder report claims modifications were authored in this PR that are completely absent from the PR branch's git diff against its base.
Risk: A reviewer or CI system auditing this PR cannot verify the production code delta from the PR diff. If merged into a clean base branch (such as `main`), the PR would deliver only documentation and a single test, failing to deliver the actual feature implementation. If merged into `c4dca4d`, the PR is redundant because the production code was already present before the PR was created.
Recommended next step: Align the branch history and documentation. Either rebase `ada09/cr-01` onto the true baseline branch that lacks CR-01 (e.g. `main` or `6c4f41d`) so that `results/pr.diff` genuinely includes the production code changes, or update `results/coder-report.md` to accurately reflect the real delta of this PR branch.

### RF-02 SHOULD FIX
Category: Test Coverage / Validation Gap
Requirement / AC: CR-01 / AC-03 / FR-01
File/Line: `tests/test_search_field_filter.py`:87-106
Evidence:
In `tests/test_search_field_filter.py`, the new test `test_find_matches_with_field_filter` verifies:
- `field="email"` (asserting match count and `MatchType.PARTIAL`)
- `field="name"` (asserting match count and `MatchType.EXACT`)
- `field="surname"` (asserting match count only: `assert len(matches_surname) == 2`)
However, `field="full_name"` is completely omitted from `test_find_matches_with_field_filter`. Furthermore, for `field="surname"`, the test fails to assert the `match_type` of the individual matches (`MatchType.EXACT` for Elton John and `MatchType.PARTIAL` for Robert Johnson).
Problem: `full_name` is one of the four supported fields in `VALID_SEARCH_FIELDS`, but its classification behavior through `find_matches()` is never verified. Additionally, the classification types for exact vs. partial matches under `field="surname"` are unasserted, creating a gap in match type verification.
Risk: A regression causing `find_matches()` to misclassify or fail when filtering by `full_name` or when distinguishing exact from partial surname matches would not be detected by automated tests.
Recommended next step: Extend `test_find_matches_with_field_filter` to test `field="full_name"` (verifying exact and/or partial matches) and assert `match_type == MatchType.EXACT` and `match_type == MatchType.PARTIAL` on the returned surname matches.

### RF-03 SHOULD FIX
Category: Test Coverage / Public API Contract
Requirement / AC: CR-01 / ARCHITECTURE.md (Search Service Interface)
File/Line: `src/customer_search/search_service.py`:238-262, `tests/test_search_field_filter.py`
Evidence:
`SearchService.get_exact_matches(query: str, field: str | None = None)` (line 238) and `SearchService.get_partial_matches(query: str, field: str | None = None)` (line 251) are public methods whose signatures were expanded to accept `field`.
In `tests/test_search_field_filter.py`, there is not a single test that invokes `get_exact_matches()` or `get_partial_matches()` with `field` specified.
Problem: The public API methods have no direct unit tests asserting that they properly filter and sort exact and partial matches when `field` is provided. They only receive indirect coverage through `search()`.
Risk: If `search()` is refactored to not delegate through `get_exact_matches()` and `get_partial_matches()`, regressions or edge cases in these public methods will not be caught.
Recommended next step: Add dedicated unit tests in `tests/test_search_field_filter.py` verifying `get_exact_matches(query, field=...)` and `get_partial_matches(query, field=...)` directly.

### RF-04 SHOULD FIX
Category: Test Coverage / Scenario Asymmetry
Requirement / AC: CR-01 / AC-01 / AC-02 / FR-02
File/Line: `tests/test_search_field_filter.py`:42-85
Evidence:
Inspecting the individual field tests in `tests/test_search_field_filter.py`:
- `test_filter_by_email_only` tests only a partial match (`"john"` in `"john.worker@example.com"`). An exact email match (e.g. searching `"john.worker@example.com"`) is never tested.
- `test_filter_by_name_only` tests only an exact match (`"john"` vs `"John"`). A partial name match (e.g. searching `"joh"`) is never tested.
- `test_filter_by_full_name_only` tests only an exact match (`"Elton John"` vs `"Elton John"`). A partial full-name match is never tested.
Problem: For three of the four supported fields, the test suite only tests one half of the matching spectrum (either exact-only or partial-only).
Risk: Incomplete verification allows potential bugs in field-specific exact matching on email or field-specific substring matching on name/full_name to escape detection.
Recommended next step: Supplement field filter tests with both exact and partial match test cases for each supported field in `VALID_SEARCH_FIELDS`.

### RF-05 SHOULD FIX
Category: Technical Debt / Performance & Design
Requirement / AC: CR-01 / NFR-02 (Support up to 10,000 customers)
File/Line: `src/customer_search/search_service.py`:156-160, 227-230, 246, 259, 288-295
Evidence:
1. In `src/customer_search/search_service.py`, `field in VALID_SEARCH_FIELDS` validation is checked redundantly across multiple layers:
   - Line 325 in `execute_search()`
   - Line 288 in `search()`
   - Line 227 in `find_matches()`
   - Line 156 in `classify_match()` inside the inner loop over all customer records.
   For a search over 10,000 customers (NFR-02), the membership test `field not in VALID_SEARCH_FIELDS` is evaluated more than 20,000 times per query.
2. In `search()` (lines 293-294):
   ```python
   exact_sorted = self.get_exact_matches(query, field=field)
   partial_sorted = self.get_partial_matches(query, field=field)
   ```
   Both `get_exact_matches()` and `get_partial_matches()` call `self.find_matches(query, field=field)`. Each call iterates over every customer record and executes `classify_match()`. Consequently, every customer is evaluated and classified twice, even though a single pass of `find_matches()` already partitions customers into `EXACT` and `PARTIAL`.
Problem: Inefficient design with repeated validation inside O(N) loops and duplicate full-dataset iterations per search call.
Risk: Unnecessary CPU cycle consumption and latency degradation when searching large customer datasets near the NFR-02 threshold (10,000 records).
Recommended next step: Call `find_matches()` once inside `search()`, partition the returned `CustomerMatch` list into exact and partial lists in a single pass, and remove redundant `VALID_SEARCH_FIELDS` checks inside the inner `classify_match()` loop once input validation has passed at the service boundary.

### RF-06 OPTIONAL
Category: Code Quality / Maintainability
Requirement / AC: CR-01 / SR-04 (Case Insensitivity & Normalization)
File/Line: `src/customer_search/search_service.py`:87-92, 166-179
Evidence:
`normalize_text(text: str) -> str` is defined at line 87:
```python
def normalize_text(text: str) -> str:
    return text.strip().lower()
```
In `classify_match()`, line 161 properly calls `normalized_query = normalize_text(query)`. However, lines 166-179 manually repeat `.strip().lower()` 8 separate times across the conditional branches:
```python
    if field == "name":
        searchable_fields = [customer.name.strip().lower()]
    elif field == "surname":
        searchable_fields = [customer.surname.strip().lower()]
    elif field == "full_name":
        searchable_fields = [customer.full_name.strip().lower()]
    elif field == "email":
        searchable_fields = [customer.email.strip().lower()]
    else:
        searchable_fields = [
            customer.name.strip().lower(),
            customer.surname.strip().lower(),
            customer.full_name.strip().lower(),
            customer.email.strip().lower(),
        ]
```
Problem: Duplicated inline string normalization logic bypassing the existing domain helper function `normalize_text()`.
Risk: If normalization rules are updated in `normalize_text()` (e.g. adding unicode NFKD decomposition), the customer field normalization will diverge from query normalization.
Recommended next step: Refactor lines 166-179 to use `normalize_text(customer.name)`, `normalize_text(customer.surname)`, etc.

### RF-07 OPTIONAL
Category: Code Quality / Maintainability
Requirement / AC: CR-01
File/Line: `src/customer_search/search_service.py`:14, 132, 213, 241, 254, 268, 302
Evidence:
Line 14 imports:
```python
from dataclasses import dataclass, field
```
`field` from `dataclasses` is used in the definition of `SearchResult` at line 82 (`customers: list[Customer] = field(default_factory=list)`).
In subsequent functions (lines 132, 213, 241, 254, 268, 302, 359, 371), the parameter name `field: str | None = None` shadows the imported `dataclasses.field` symbol.
Problem: Local function parameter shadows a module-level import.
Risk: Although harmless at runtime because `dataclasses.field` is only evaluated at class decoration time, symbol shadowing impairs code clarity and can lead to bugs if future class definitions or helper utilities are added below these functions.
Recommended next step: Import `dataclasses` directly or import `field as dc_field`, or rename parameter or import to eliminate shadowing.

## Missing Evidence / Open Questions
1. Target PR Integration Branch: What is the intended upstream target branch for PR candidate `ada09/cr-01`? If the target branch is `origin/ada09/cr_01`, the PR contains no production changes. If the target branch is `main` (which sits at commit `0f6af39`), the branch contains extensive unmerged commits from ADA-08 that are not covered in `CHANGE_REQUEST.md`. Clarification of the base and merge target is required.
2. Performance Benchmark for Field Filter with 10,000 Customers: While `test_load_up_to_10000_customers_performance` tests loading performance, there is no benchmark in the verification report specifically measuring `search(..., field=...)` response times against 10,000 customer records to verify that repeated field validation and double iteration remain within NFR-01 (< 2 seconds).

## Summary
MUST FIX: 1
SHOULD FIX: 4
OPTIONAL: 2

## Reviewer Recommendation
- [ ] NOT READY
- [x] READY AFTER MUST FIX
- [ ] READY FOR HUMAN REVIEW

This recommendation is not a merge approval.
