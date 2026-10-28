# Repository Readiness Audit

## BEFORE

| Dimension                   | Score 0-5 | Weighted | Evidence | Main Gap |
| --------------------------- | --------: | -------: | -------- | -------- |
| Entry Point & Navigation    |         4 | 12.00/15 | `README.md` includes Table of Contents, project structure tree, setup/run commands, and links to docs (`docs/traceability.md`, `results/agent-report.md`). | Lacks an agent-specific root manifest/onboarding file detailing environment nuances (e.g., Windows CRLF, PowerShell syntax) and explicit conflict resolution hierarchy between documents. |
| Agent Instructions          |         3 |  9.00/15 | `AGENTS.md` defines 9 project rules, validation steps, and Definition of Done. | Lacks concrete operational command snippets, explicit negative file boundaries (e.g., do not touch `data/customers.json`), git workflow conventions, and tool/environment guidance. |
| Build / Run / Test          |         4 | 12.00/15 | `pyproject.toml` configures pytest and pythonpath; tests run via `pytest` in 0.75s; standard library runtime with zero external runtime dependencies. | Absence of a unified single-command task runner (e.g. Makefile, taskfile, or runner script) and lack of pinned/lockfile dependencies or dev-dependencies specification. |
| Architecture Boundaries     |         4 |  8.00/10 | `ARCHITECTURE.md` details 5 components, explicit responsibilities, negative constraints ("shall not..."), data flow, and interfaces; domain model is `@dataclass(frozen=True)`. | Boundaries and component isolation rely entirely on documentation and developer discipline without automated import linting or architectural constraint verification. |
| Requirements & Traceability |         4 |  8.00/10 | Consistent ID taxonomy (`FR-xx`, `NFR-xx`, `SR-xx`, `VR-xx`, `EH-xx`, `AC-xx`, `TS-xx`, `T-xx`); comprehensive matrix in `docs/traceability.md`. | Traceability matrix is a static manual markdown file without automated validation tools linking test execution results to requirement IDs. |
| Automation & Guardrails     |         1 |  2.00/10 | Only `pytest` is configured. No GitHub Actions CI, no git hooks, no linters (Ruff/Flake8), no formatters (Black), no typecheckers (Mypy), and no `.gitignore` file. | Total absence of continuous integration (CI) workflows, static analysis, linting, format checks, git hooks, and `.gitignore` file (bytecode `.pyc` files are tracked in git). |
| Testability & Evidence      |         4 | 12.00/15 | 82 unit, integration, and scenario tests passing in 0.75s; mockable CLI I/O; explicit acceptance criteria coverage; execution reports in `results/`. | Absence of automated test coverage measurement (e.g. `pytest-cov` with thresholds) and machine-readable test artifacts (JUnit XML / HTML). |
| Safety & Permissions        |         2 |  4.00/10 | Read-only data design with SHA-256 hash verification in tests (`test_json_data_source_read_only`); immutable dataclass; no external APIs or secrets required. | Lack of a `.gitignore` file (polluting git with binaries/cache), absence of automated secret/leak scanning, and absence of filesystem-level write protection on data files. |

TOTAL BEFORE: 67.00 / 100

Top 3 friction points:
1. **Total absence of CI workflows, linters, type checking, and git hooks (Automation & Guardrails)**: The repository relies solely on manually executing `pytest`. There are no automated checks for code style, type soundness, formatting, or regression prevention prior to commit or push.
2. **Missing `.gitignore` causing cache pollution and repository hygiene risks (Safety & Permissions / Automation & Guardrails)**: Because `.gitignore` does not exist, compiled bytecode (`__pycache__/*.pyc`) is actively tracked by git, creating noise in diffs and risking inadvertent commits of local artifacts or sensitive data.
3. **Lack of operational recipes, environment specifics, and file boundaries in `AGENTS.md` (Agent Instructions)**: While `AGENTS.md` outlines general rules, it omits actionable tool commands, OS/shell considerations (such as Windows CRLF handling and PowerShell argument parsing), and explicit read-only file protection constraints (e.g. `data/customers.json`).

---

### Justification of Scores

- **Entry Point & Navigation (4/5):** The repository provides clean, readable entry documentation in `README.md` with file tree breakdowns and execution examples. It falls short of 5 because there is no single-point agent onboarding guide that addresses tool usage, execution paths, and document hierarchy.
- **Agent Instructions (3/5):** `AGENTS.md` sets clear expectations and a Definition of Done, but is high-level (30 lines). 
- **Build / Run / Test (4/5):** The build and test workflow is simple, fast, and reproducible via standard Python and `pytest`. It loses one point because there is no unified build/task runner script and development dependencies are not formally locked or specified.
- **Architecture Boundaries (4/5):** The architecture is thoroughly documented in `ARCHITECTURE.md` with explicit component boundaries and negative constraints. However, boundary enforcement is purely conceptual and not guarded by automated structural tests or import linter rules.
- **Requirements & Traceability (4/5):** Requirements, specifications, tasks, and tests share a coherent ID taxonomy, summarized in `docs/traceability.md`. It lacks a 5th point because traceability is manually tracked and not verified via automated testing decorators or matrix generators.
- **Automation & Guardrails (1/5):** The repository has almost no automated guardrails beyond test execution: no CI workflows, no linters, no formatters, no type checkers, no pre-commit hooks, and no `.gitignore`.
- **Testability & Evidence (4/5):** The test suite is fast, modular, and achieves 100% pass rates across 82 tests, with deterministic CLI mocking and performance benchmarking. It lacks code coverage tooling (e.g., `pytest-cov`) and structured test report outputs (XML/HTML).
- **Safety & Permissions (2/5):** The application itself is low-risk (no external APIs, read-only customer JSON). However, safety mechanisms are limited to in-memory immutability and test assertions. There is no `.gitignore`, no secret scanner, and no OS-level filesystem protection.
