# Review Contract

## Change
CR-01

## Requirements / Acceptance Criteria
FR-01, FR-02: Search customers by name, surname, full name, or email address (FR-01) and support partial substring matching across fields (FR-02).
AC-01, AC-02, AC-03: Search by customer name (AC-01), search by email address (AC-02), and substring search across all searchable fields (AC-03).

## Architecture Constraints
Expected dependency flow: CLI -> Search Service -> Customer Data Loader -> Customer Model (strict top-to-bottom layering; lower layers have no dependencies on upper layers; runtime relies exclusively on Python standard library).
Business-rule location: Query validation, attribute normalization, field filtering (VALID_SEARCH_FIELDS), exact/partial match classification, result ordering, and result limit (MAX_RESULTS = 10) are located exclusively in Search Service (src/customer_search/search_service.py). Data loading and JSON schema validation reside in Customer Data Loader (src/customer_search/data_loader.py). Domain representation and full_name property reside in Customer Model (src/customer_search/customer.py). CLI (src/customer_search/cli.py) manages I/O and display formatting only.
Protected boundaries: data/customers.json (strictly read-only local JSON file with filesystem-level protection and SHA-256 hash checks); authoritative specification documents (REQUIREMENTS.md and SPEC.md are immutable); runtime dependency boundary (Python standard library only; zero external runtime dependencies); test suite integrity (existing tests must not be deleted, weakened, or bypassed; coverage must remain >= 90%); public API export parity (search.py, loader.py, models.py, and __init__.py must mirror core module exports).

## Review Rules
- Verify requirement coverage.
- Verify every called API/dependency exists.
- Check architecture boundaries.
- Inspect tests for masking false confidence.
- Check regression behavior.
- Identify unnecessary technical debt.
- Cite evidence for every finding.

## Severity
- MUST FIX: Requirement violation, regression, security/integrity risk, hallucinated API/dependency, broken architecture constraint, or defect that makes the change unsafe to approve.
- SHOULD FIX: Significant maintainability, coverage, design, or clarity issue that does not block the requested behavior.
- OPTIONAL: Non-blocking improvement outside the minimum acceptance threshold.
