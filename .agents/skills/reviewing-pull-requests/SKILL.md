---
name: reviewing-pull-requests
description: |
  Reviews a pull request for engineering readiness against repository specifications, requirements, code changes, and test evidence.
  Use when the user asks to:
  - Review a pull request or PR diff.
  - Assess PR readiness, test coverage, or acceptance criteria compliance.
  - Check changes against SPEC.md, REQUIREMENTS.md, or ARCHITECTURE.md.
  - Generate an engineering review report or audit summary for a PR.
  Do NOT use when the user wants to:
  - Implement feature code, bugfixes, or refactor existing code.
  - Post comments, approve, or merge pull requests via the GitHub API.
  - Resolve git merge conflicts or teach generic Git commands.
metadata:
  owner: Ashley Shaden Aguilar Moreno
  course: UADY-IS-AI
  version: 1.0.1
---

# Reviewing Pull Requests

## When to use
Use this skill for PR readiness reviews before human approval.

## Preconditions
- The target repository, branch, or PR diff is accessible locally or remotely.
- Read-only inspection is sufficient (no active code editing requested).
- If REQUIREMENTS.md, SPEC.md, or ARCHITECTURE.md exist, they serve as the authoritative, normative context.

## Workflow

1. **Identify Target PR / Diff**
  - Identify the source and target branches, commits, or pull request diff to be inspected.
  - List all modified, added, and deleted files.

2. **Read Normative Context & Specifications**
  - Review project instructions (e.g., AGENTS.md).
  - Read REQUIREMENTS.md and SPEC.md to understand expected behaviors and acceptance criteria.
  - Read ARCHITECTURE.md to identify constraints, layer boundaries, and patterns.

3. **Inspect Changed Files & Trace Behavior**
  - Review file diffs line by line.
  - Map every code modification directly to the corresponding acceptance criteria or functional requirements.
  - Flag undocumented side effects, unnecessary refactors, or out-of-scope changes.

4. **Inspect and Run Relevant Tests**
  - Run the test suite (e.g., `pytest`) to verify current pass/fail status and regression safety.
  - Confirm that new behaviors are explicitly asserted with positive and negative test cases.
  - Verify that test assertions are meaningful and not weakened or bypassed.

5. **Apply Review Checklist**
  - Consult and evaluate each item defined in references/review_checklist.md.
  - Verify code hygiene, error handling, edge cases, and documentation parity.

6. **Classify Findings by Severity**
  - Evaluate all discovered issues using references/severity_guide.md.
  - Classify each finding according to the defined severity criteria.

7. **Draft the Review Report**
  - Generate the draft report using the structure from assets/review_report_template.md.
  - Write the draft to: `results/pr-readiness-review.md`

8. **Validate the Report Format**
  - Execute the validation script against the generated report:
    ```bash
    python scripts/validate_review_report.py results/pr-readiness-review.md
    ```

9. **Self-Correction & Repair Loop**
  - If validation errors or schema mismatches are reported:
  - Review the script error output.
  - Edit `results/pr-readiness-review.md` to resolve missing sections, malformed tables, or invalid classifications.
  - Re-run `python scripts/validate_review_report.py results/pr-readiness-review.md` until it exits successfully.

10. **Human Reviewer Handover**
  - Halt autonomous execution.
  - Present the final review summary and readiness recommendation to the human reviewer for final decision.

## Safety / Boundaries
- **Read-only execution:** Never alter production code, refactor implementation files, or apply fixes during this review.
- **No GitHub side-effects:** Do NOT post comments, approve, or merge Pull Requests via CLI or API.
- **Test integrity:** Never delete, weaken, mock out, or bypass failing tests to eliminate findings.
- **Specification conflict protocol:** If REQUIREMENTS.md and SPEC.md contradict each other, stop immediately and escalate the discrepance under `Human decision required`.

## Output
Save the final report to: `results/pr-readiness-review.md`

The report must distinguish:
- MUST FIX
- SHOULD FIX
- OPTIONAL
- Human decision required
