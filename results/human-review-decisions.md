# Human Review Decisions

## Change
CR-01

### RF-01
Reviewer severity: MUST FIX
Human decision: ACCEPTED
Reason:
- Evidence summary: In `results/coder-report.md` (lines 73-90), the coder agent claims to have modified `src/customer_search/search_service.py`, `src/customer_search/search.py`, `src/customer_search/__init__.py`, and added 10 unit tests. However, `results/pr.diff` (git diff between base `c4dca4d` and commit `b4134e6`) contains zero changes to `src/` files and only 1 new test in `tests/test_search_field_filter.py`. The production code changes and 9 of the tests were already committed in ancestor commit `5454747` prior to base commit `c4dca4d`.
- Reviewer recommendation: Align branch history or documentation. Either rebase `ada09/cr-01` onto the clean base branch lacking CR-01 (e.g., `main` or `6c4f41d`) so that `results/pr.diff` contains the actual production implementation, or update `results/coder-report.md` to accurately describe the branch's real delta.
- Proposed decision (Recommendation): ACCEPT as MUST FIX. The PR candidate cannot be approved for merge if the PR diff does not contain the feature implementation claimed in the coder report.
Required action: Clarify the target base branch with the human lead, rebase the branch if necessary, or update `results/coder-report.md` and `results/pr.diff` to accurately reflect the true change delta.

### RF-02
Reviewer severity: SHOULD FIX
Human decision: ACCEPTED
Reason:
- Evidence summary: In `tests/test_search_field_filter.py` (lines 87-106), `test_find_matches_with_field_filter` tests `email`, `name`, and `surname`, but completely omits `field="full_name"`. In addition, for `field="surname"`, it only asserts match count (`len == 2`) without verifying the classification type (`match_type == MatchType.EXACT` vs. `MatchType.PARTIAL`).
- Reviewer recommendation: Extend `test_find_matches_with_field_filter` to include `field="full_name"` and assert explicit `match_type` values for exact and partial surname matches.
- Proposed decision (Recommendation): ACCEPT. Adding coverage for all valid fields and verifying match types prevents regressions in `find_matches()`.
Final severity: PENDING CONFIRMATION (Proposed: SHOULD FIX)
Required action: Update `tests/test_search_field_filter.py` to add `field="full_name"` test cases and explicit assertions for `MatchType.EXACT` and `MatchType.PARTIAL` in `test_find_matches_with_field_filter`.

### RF-03
Reviewer severity: SHOULD FIX
Human decision: ACCEPTED
Reason:
- Evidence summary: In `src/customer_search/search_service.py` (lines 238-262), `get_exact_matches(query, field=...)` and `get_partial_matches(query, field=...)` are public methods whose signatures accept the new `field` parameter, but neither method is directly tested with `field` in `tests/test_search_field_filter.py`.
- Reviewer recommendation: Add dedicated unit tests verifying that `get_exact_matches()` and `get_partial_matches()` filter and sort correctly when `field` is specified.
- Proposed decision (Recommendation): ACCEPT. Direct testing of public API contracts ensures robustness against future refactoring of `search()`.
Final severity: PENDING CONFIRMATION (Proposed: SHOULD FIX)
Required action: Add direct unit tests in `tests/test_search_field_filter.py` invoking `get_exact_matches` and `get_partial_matches` with `field` parameters.

### RF-04
Reviewer severity: SHOULD FIX
Human decision: ACCEPTED
Reason:
- Evidence summary: In `tests/test_search_field_filter.py` (lines 42-85), individual field tests are asymmetric: `test_filter_by_email_only` tests only a partial match (no exact match); `test_filter_by_name_only` tests only an exact match (no partial match); `test_filter_by_full_name_only` tests only an exact match (no partial match).
- Reviewer recommendation: Supplement unit tests to verify both exact and partial matches across all four supported fields (`name`, `surname`, `full_name`, `email`).
- Proposed decision (Recommendation): ACCEPT. Ensures comprehensive test coverage across both match classifications for every searchable attribute.
Final severity: PENDING CONFIRMATION (Proposed: SHOULD FIX)
Required action: Add test cases in `tests/test_search_field_filter.py` covering exact email search, partial name search, and partial full_name search with `field` filter enabled.

### RF-05
Reviewer severity: SHOULD FIX
Human decision: ACCEPTED
Reason:
- Evidence summary: In `src/customer_search/search_service.py` (lines 156-160, 227-230, 288-295), `field in VALID_SEARCH_FIELDS` is checked redundantly at every layer and inside the loop for every customer in `classify_match()` (>20,000 checks for 10,000 customers). Furthermore, `search()` calls `get_exact_matches()` and `get_partial_matches()`, which each call `find_matches()`, causing two full iterations over the entire customer list and classifying each customer twice per search.
- Reviewer recommendation: Refactor `search()` to call `find_matches()` once and partition results into exact and partial lists in memory, and eliminate redundant static validation inside the inner matching loop.
- Proposed decision (Recommendation): ACCEPT as SHOULD FIX, or DEFER to a dedicated optimization task if human lead prioritizes immediate feature delivery over performance refactoring.
Final severity: PENDING CONFIRMATION (Proposed: SHOULD FIX)
Required action: Determine whether to refactor `search()` and `classify_match()` now or track as technical debt for subsequent iteration.

### RF-06
Reviewer severity: OPTIONAL
Human decision: ACCEPTED
Reason:
- Evidence summary: In `src/customer_search/search_service.py` (lines 166-179), `classify_match()` calls `.strip().lower()` manually 8 times across branches instead of reusing the existing helper function `normalize_text()`.
- Reviewer recommendation: Refactor lines 166-179 to use `normalize_text(customer.name)`, etc.
- Proposed decision (Recommendation): ACCEPT as non-blocking code quality improvement.

### RF-07
Reviewer severity: OPTIONAL
Human decision: ACCEPTED
Reason:
- Evidence summary: In `src/customer_search/search_service.py` (lines 14, 132, 213, 241, 254, 268, 302), function parameter `field` shadows `dataclasses.field` imported at line 14.
- Reviewer recommendation: Import `dataclasses` directly or use `from dataclasses import field as dc_field` to eliminate identifier shadowing.
- Proposed decision (Recommendation): ACCEPT as non-blocking code quality improvement.

## Human Gate
- [X] Return to coder-agent
- [ ] Ready for final re-review
- [ ] Stop / escalate
