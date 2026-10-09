# PR Review Checklist

Use this checklist during Step 5 of the Pull Request review workflow to systematically audit changes against software engineering standards, repository specifications, and quality gates.

## Requirements / Specification
- [ ] **Traceability:** Every changed behavior directly maps to an existing Requirement or Acceptance Criterion in `REQUIREMENTS.md` / `SPEC.md`.
- [ ] **No Undocumented Rules:** No undocumented business rules, covert assumptions, or hidden requirements are introduced in the implementation.
- [ ] **Specification Consistency:** Implementation and `SPEC.md` are completely consistent (naming, signatures, error codes, and edge-case contracts).

## Code
- [ ] **Focus and Scope:** The change is cohesive, focused, and understandable; it addresses only the designated issue/scope.
- [ ] **Error Handling:** Exceptions, edge cases, and unexpected inputs are handled gracefully and safely.
- [ ] **No Unrelated Refactoring:** No unrelated code formatting, cosmetic refactoring, or collateral modifications are mixed into the PR.
- [ ] **Dependencies Justified:** No new dependencies, libraries, or external packages are introduced unless strictly justified and approved.
- [ ] **Repository Hygiene:** No transient or build artifacts (e.g., `__pycache__`, `.pyc`, debug logs, temporary files) are committed.

## Tests
- [ ] **Automated Evidence:** All new, modified, or bugfixed behaviors are backed by automated tests.
- [ ] **Edge Cases Covered:** Boundary conditions, empty inputs, whitespace, malformed payloads, and limit values have test coverage.
- [ ] **No Test Weakening:** Existing tests have not been deleted, loosened, bypassed, or weakened to mask regressions.
- [ ] **Behavior vs Implementation:** Tests verify observable system behavior and contracts, not internal private implementation details.
- [ ] **Suite Execution:** The entire automated test suite passes cleanly without regressions or flaky failures.

## Architecture
- [ ] **Boundary Compliance:** Modifications respect documented architectural layer boundaries, modular encapsulation, and patterns in `ARCHITECTURE.md`.
- [ ] **Architectural Parity:** If the structural design, interfaces, or module relationships changed, `ARCHITECTURE.md` is updated synchronously.

## Security
- [ ] **Credential Protection:** No secrets, tokens, API keys, passwords, or sensitive credentials are committed.
- [ ] **Least Privilege:** No unnecessary permissions, insecure file operations, or elevated privileges are requested or granted.
- [ ] **Input Validation & Sanitization:** All external and user-supplied inputs are validated and sanitized before processing.

## Evidence
- [ ] **Grounded Findings:** Every review finding explicitly cites concrete evidence (file paths, line numbers, test output, or conflicting specification clauses).
