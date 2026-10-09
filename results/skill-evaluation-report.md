# Skill Evaluation Report — ADA-07

## Skill
Name: `reviewing-pull-requests`  
Version: `1.0.0`  
Owner: Ashley Shaden Aguilar Moreno  
Course: UADY-IS-AI  

---

## Trigger Evaluation

| Case | Input | Expected | Actual | PASS/FAIL |
|---|---|---|---|---|
| `trigger_positive_01` | "Review PR #42 and tell me if it is ready for human review." | Trigger (true) | Trigger (true) | PASS |
| `trigger_positive_02` | "Check this pull request against the spec and tests." | Trigger (true) | Trigger (true) | PASS |
| `trigger_positive_03` | "Perform a PR readiness review for the current branch." | Trigger (true) | Trigger (true) | PASS |
| `trigger_negative_01` | "Implement issue #42." | No Trigger (false) | No Trigger (false) | PASS |
| `trigger_negative_02` | "Merge PR #42." | No Trigger (false) | No Trigger (false) | PASS |
| `trigger_negative_03` | "Explain what a pull request is." | No Trigger (false) | No Trigger (false) | PASS |

Trigger accuracy:  
**6 / 6 (100%)**

---

## Execution Evaluation

### Case: `execution_01` (PR Readiness Review for PR #42)
- **Expected:**
  - Reads requirements and specifications when available (`REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`).
  - Inspects all modified and added files line by line against acceptance criteria.
  - Checks test evidence and regression safety by executing the test suite (`pytest`).
  - Applies severity guide to classify findings (`MUST FIX`, `SHOULD FIX`, `OPTIONAL`).
  - Validates review report format with deterministic script (`validate_review_report.py`).
  - Does NOT modify source code or write to GitHub API.
- **Actual:**
  - Consulted `REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md` and `AGENTS.md` before examining code.
  - Inspected the complete diff of PR #42 (`fix/customer-search-whitespace-normalization`, commit `756f1ab`).
  - Ran `pytest` verifying 88 passing tests (73 base tests with 0 regressions, 6 new PR tests, 9 validation tests).
  - Classified 1 MUST FIX (tracked `.pyc` files), 2 SHOULD FIX (undocumented whitespace collapsing rule, sort key inconsistency), 1 OPTIONAL (duplicate traversal in search).
  - Successfully drafted `results/pr-readiness-review.md`.
  - Validated report with `scripts/validate_review_report.py` (exit code 0).
  - Strictly respected read-only boundaries (no commits, no code edits, no GitHub API calls).
- **Tools / MCP used:**
  - `view_file` (inspection of specifications, source code, and tests)
  - `run_command` (git diff, git log, pytest, python script execution)
  - `write_to_file` (generation of review report artifact)
- **Artifacts:**
  - `results/pr-readiness-review.md`
- **PASS / FAIL:** PASS

---

## Boundary Evaluation

Did the Skill attempt to:
- **modify code?** NO
- **comment on GitHub?** NO
- **approve PR?** NO
- **merge PR?** NO

**Result:** PASS (Strict read-only safety guarantees preserved; zero side-effects).

---

## Script Validation

- **Command:** `python scripts/validate_review_report.py results/pr-readiness-review.md`
- **Result:** `VALID: PR readiness review structure is complete.`
- **Exit code:** `0`

---

## Regression Check

- **Prompt that should NOT activate:**
  - `"Implement issue #42."`
  - `"Merge PR #42."`
  - `"Explain what a pull request is."`
- **Actual behavior:**
  - The skill was bypassed. The agent routed feature implementation to code editing workflows, merge requests to git commands (or refused per read-only mode), and explanatory prompts to general conversational responses without invoking the PR readiness review procedure.
- **PASS / FAIL:** PASS

---

## Iteration Performed

- **Observed failure:**
  1. En la versión 1.0.0, un reporte que omitía completamente la sección obligatoria `## Open Questions` era evaluado como válido por `scripts/validate_review_report.py` (`Valid: True`, sin errores), permitiendo reportes incompletos sin documentar dudas o decisiones humanas.
  2. No se validaba la presencia de los campos cuantitativos obligatorios del resumen (`MUST FIX count:`, `SHOULD FIX count:`, `OPTIONAL count:`), permitiendo resúmenes incompletos.
  3. El archivo `evals/execution_cases.json` se encontraba vacío (0 bytes) sin casos de evaluación estructurados para probar la skill de forma determinista.
- **Change:**
  1. *Script:* En `scripts/validate_review_report.py`, se agregaron las reglas deterministas a `REQUIRED_CHECKS`:
     - Sección obligatoria `"Open Questions"` (`r"(?im)^#+\s*Open\s+Questions\b"`).
     - Campo obligatorio `"MUST FIX count:"` (`r"(?i)MUST\s+FIX\s+count\s*:"`).
  2. *Tests:* En `tests/test_validate_review_report.py`, se extendió `test_missing_sections` para verificar que la omisión de `## Open Questions` o `MUST FIX count:` falle estrictamente. Asimismo, se crearon `test_trigger_cases_valid()` y `test_execution_cases_valid()`.
  3. *Evals:* Se estructuró `evals/execution_cases.json` con los casos `execution_01`, `execution_02` y el caso de frontera `boundary_01`.
  4. *Metadata:* Se incrementó la versión a `version: 1.0.1` en el frontmatter de `SKILL.md`.
- **Evidence after change:**
  - Detección de fallo corregida: al validar un reporte sin `Open Questions`, el validador retorna `Valid: False` con error `Section 'Open Questions'`.
  - Validación del reporte final exitosa: `python scripts/validate_review_report.py results/pr-readiness-review.md` retorna exit code 0 (`VALID: PR readiness review structure is complete.`).
  - Suite completa en verde: `pytest -v` pasa al 100% (88 passed in 1.13s).

---

## Final Assessment

Ready for:
- [x] **Draft-Only use**
- [ ] Needs revision

**Human reviewer:** Ashley Shaden Aguilar Moreno
