# Finding Severity Guide

Use this guide during Step 6 of the Pull Request review workflow to classify all review findings consistently and objectively.

## MUST FIX
Use when the change:
- Violates a Requirement or Acceptance Criterion.
- Introduces a regression in existing behavior.
- Breaks tests required by the specification.
- Creates a security or data integrity problem.
- Makes the PR unsafe to approve.

## SHOULD FIX
Use when the feature can work, but there is a significant maintainability, testability, architecture, or clarity problem:
- Code clarity, maintainability, or readability risks.
- Architectural boundary friction or modular coupling.
- Test design issues (e.g., fragile assertions, untested non-critical paths).
- Inconsistent internal patterns or redundant computations.

## OPTIONAL
Use for non-blocking improvements that do not affect the approved behavior or safety:
- Minor stylistic preferences or cosmetic adjustments.
- Non-essential refactoring ideas.
- Micro-optimizations with negligible impact.

## Human Decision Required
Use when an issue cannot be resolved by objective code inspection and requires a human stakeholder's sign-off:
- Ambiguities or direct conflicts between `REQUIREMENTS.md` and `SPEC.md`.
- Unclear product behavior where trade-offs must be evaluated.
- Decisions on whether undocumented implementation behavior should be formally adopted into the specification.

---

> [!IMPORTANT]
> **Evidence Rule:** Every finding must contain concrete, verifiable evidence (file path, line number, test result, or specification citation). Unsubstantiated claims are not valid findings.
