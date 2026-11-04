# Change Request

Change ID: CR-01

## Goal

Add an optional field filter parameter (`field`) to the customer search service operations (`search`, `find_matches`, and `execute_search`), allowing callers to restrict search matching to a specific customer attribute (`"name"`, `"surname"`, `"full_name"`, or `"email"`). When `field` is omitted or `None`, the search shall preserve its default behavior of evaluating across all searchable attributes.

## Requirements Covered

FR-01
FR-02
AC-01
AC-02
AC-03

## Constraints

Follow AGENTS.md.
Use REQUIREMENTS.md and SPEC.md as the source of truth.
Preserve architecture boundaries.
Do not weaken existing tests.

## Verification

- Automated tests verify that specifying `field="email"` returns only customers whose email matches the query, even if the query matches another customer's name or surname.
- Automated tests verify that specifying `field="name"` returns only customers whose first name matches the query.
- Automated tests verify that specifying `field="surname"` returns only customers whose surname matches the query.
- Automated tests verify that specifying `field="full_name"` returns only customers whose full name matches the query.
- Automated tests verify that omitting `field` or passing `field=None` retains the existing behavior across all searchable fields without regression.
- Automated tests verify that providing an unsupported field name raises a `ValueError`.
- All existing tests in the test suite continue to pass.

## Human Approval

Approved to implement: YES
Approved by: Ashley Aguilar 
Date: 03/11/2026
