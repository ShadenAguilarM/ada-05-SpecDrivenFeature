# Implicit Knowledge Found

## IK-01

**What:**
Source and test files in this repository use Windows CRLF (`\r\n`) line endings rather than Unix LF (`\n`). Text-replacement and diff-patching tools that expect standard Unix newlines fail when matching target blocks.

**Evidence:**
- In `results/before-agent-run.md`, the `edit_file` tool call failed when attempting to update `src/customer_search/search_service.py` with the error message: `Encountered error in tool execution: target content not found in the file; the Target must exactly match existing file text, including whitespace`.
- Verified via PowerShell command: `python -c "with open('src/customer_search/search_service.py', 'rb') as f: print(repr(f.readline()))"`, which output `b'"""Customer search service module.\r\n'`.

**How was it discovered:**
The agent discovered this through an unexpected tool failure during `edit_file` execution, followed by inspecting the raw binary representation of the file's line endings using a Python one-liner.

**Risk:**
Agents attempting granular file modifications using text replacement tools or diffs will fail repeatedly, wasting interaction cycles or resorting to rewriting entire files, which increases the risk of accidental regressions.

**Should this remain implicit?**
NO. Tooling assumptions regarding line endings directly affect an agent's ability to safely edit code in the repository.

**Where should it become explicit?**
- `AGENTS.md` (in an environment/tooling guidance section).
- `.gitattributes` at the repository root.

**Remediation:**
Add a `.gitattributes` file configuring line-ending normalization (e.g. `* text=auto eol=lf` or consistent checkout policies) and document in `AGENTS.md` that files in this workspace currently use CRLF and require whole-file replacement or CRLF-compatible matching.

---

## IK-02

**What:**
PowerShell strips empty string arguments (`""`) when passing parameters to Python scripts from the command line, causing `sys.argv[1:]` to be empty and forcing interactive CLI scripts to prompt for stdin rather than receiving an empty argument.

**Evidence:**
- Documented in `results/agent-report.md` under Problem 3: "PowerShell Argument Stripping on Empty String (T-07): Invoking `python src/customer_search/cli.py ""` in PowerShell stripped the empty string argument, causing the CLI to interpret it as having zero arguments and enter the interactive input loop."
- In `src/customer_search/cli.py`, `run_search_cli` checks `if args and len(args) > 0:` to decide whether to process arguments or prompt interactively via `input_func`.

**How was it discovered:**
Discovered during task T-07 when attempting to validate empty-string CLI behavior from a PowerShell terminal, resulting in an unresponsive process waiting for user input.

**Risk:**
An agent attempting to validate CLI input validation rules (such as FR-08 / AC-09) via direct CLI subprocess invocation in PowerShell will experience hangs or process timeouts, falsely reporting test failures or deadlocking automated workflows.

**Should this remain implicit?**
NO. Command-line validation behavior differs across operating systems and shells, making explicit execution instructions essential for automated agents.

**Where should it become explicit?**
- `AGENTS.md` (under Execution / CLI Testing guidelines).
- `README.md` (under Execution > Behavior and Display Rules).

**Remediation:**
Document in `AGENTS.md` that empty string arguments are stripped by PowerShell, instructing agents to test validation scenarios using automated pytest fixtures with injected `input_func` (as in `tests/test_cli.py`) or explicit shell escaping (e.g. `'""'`).

---

## IK-03

**What:**
The Python execution environment requires different pathing strategies depending on invocation mode: `pytest` automatically resolves imports because `pyproject.toml` configures `pythonpath = ["src"]`, but running `python -m customer_search` requires manually setting `PYTHONPATH=src`, and running `python src/customer_search/cli.py` directly requires an internal `sys.path` fallback.

**Evidence:**
- `pyproject.toml` contains `[tool.pytest.ini_options] pythonpath = ["src"]`.
- `README.md` line 142 states: `(Note: If running as a module without installing the package, set PYTHONPATH=src)`.
- `src/customer_search/cli.py` contains lines 16–20:
  ```python
  if __package__ is None or __package__ == "":
      src_dir = str(Path(__file__).resolve().parent.parent)
      if src_dir not in sys.path:
          sys.path.insert(0, src_dir)
  ```
- In `results/agent-report.md` Problem 2: "Standalone Script Execution Pathing (T-07): Executing `python src/customer_search/cli.py "John"` directly failed with `ModuleNotFoundError: No module named 'customer_search'` because `sys.path[0]` pointed to `src/customer_search/` instead of `src/`."

**How was it discovered:**
Discovered when the agent executed standalone scripts outside of `pytest` during previous task runs, requiring an in-code `sys.path` patch, and confirmed by reviewing `README.md` and `pyproject.toml`.

**Risk:**
An agent attempting to run smoke tests, benchmark scripts, or module entry points outside of pytest may encounter `ModuleNotFoundError` and mistakenly attempt to alter package imports or create redundant setup files.

**Should this remain implicit?**
NO. A developer knows how `PYTHONPATH` affects package resolution in this layout, but an agent needs a single, canonical execution command.

**Where should it become explicit?**
- `AGENTS.md` (under Build / Run / Test recipes).
- `pyproject.toml` (by adding an editable install command or entry-point console script definition).

**Remediation:**
Add explicit instructions in `AGENTS.md` explaining that `pytest` is the primary execution harness (pre-configured with `pythonpath = ["src"]`), and recommend running `pip install -e .` or defining console scripts under `[project.scripts]` in `pyproject.toml`.

---

## IK-04

**What:**
The file `data/customers.json` serves as the feature's read-only customer database and must never be edited, generated, or altered during feature implementation or testing, even though it resides in a writable workspace directory without filesystem-level write protection.

**Evidence:**
- `SPEC.md` line 64: "The JSON data source is read-only for this feature. Customer records are not created, edited, or deleted by the search functionality."
- `REQUIREMENTS.md` constraint `A-01`: "Customer data shall be stored in a local JSON file."
- `tests/test_data_loader.py::test_json_data_source_read_only` computes a SHA-256 hash of `data/customers.json` before and after operations to verify that the file remains unmodified.
- `AGENTS.md` does not list `data/customers.json` in its project rules or file boundary guidelines.

**How was it discovered:**
The agent inferred this restriction only after reading deep into `SPEC.md` and inspecting test assertions in `tests/test_data_loader.py`. `AGENTS.md` provides no explicit list of immutable files.

**Risk:**
An agent tasked with adding features (such as adding customer fields or creating new test data) might directly modify `data/customers.json`, immediately breaking the SHA-256 baseline hash test and violating specification rule A-01.

**Should this remain implicit?**
NO. Files that function as immutable test fixtures must be explicitly protected against modification.

**Where should it become explicit?**
- `AGENTS.md` (under Project Rules and Negative Constraints / Off-Limits Files).
- `ARCHITECTURE.md` (under Data Source boundaries).

**Remediation:**
Explicitly declare in `AGENTS.md` that `data/customers.json` is an immutable baseline dataset that must never be modified by agents, and instruct agents to create temporary JSON files in pytest fixtures (e.g. `tmp_path`) for custom testing.

---

## IK-05

**What:**
The package utilizes a dual module structure with implementation modules (`search_service.py`, `data_loader.py`, `customer.py`) paired with alias modules (`search.py`, `loader.py`, `models.py`), in addition to package root exports in `__init__.py`. When introducing or modifying public functions, types, or constants, exports must be maintained across all three layers.

**Evidence:**
- In `src/customer_search/`:
  - `loader.py` re-exports from `data_loader.py`.
  - `models.py` re-exports from `customer.py`.
  - `search.py` re-exports from `search_service.py`.
  - `__init__.py` re-exports symbols from `cli.py`, `customer.py`, `data_loader.py`, and `search_service.py`.
- During the BEFORE implementation of `CR-01`, adding `VALID_SEARCH_FIELDS` required modifying `search_service.py`, `search.py`, and `__init__.py` to ensure export consistency.

**How was it discovered:**
Discovered during repository exploration before making changes, by observing duplicate module names (`search.py` vs `search_service.py`) and checking their contents.

**Risk:**
An agent modifying only the primary service file (e.g. `search_service.py`) without updating `search.py` or `__init__.py` will create broken public contracts for callers importing from package aliases, causing subtle import errors or test regressions.

**Should this remain implicit?**
NO. The reason for maintaining parallel alias modules and the requirement to keep them in sync is undocumented.

**Where should it become explicit?**
- `ARCHITECTURE.md` (under Component Structure / Module Layout).
- `AGENTS.md` (under Coding Conventions).

**Remediation:**
Document the module aliasing convention in `ARCHITECTURE.md` and `AGENTS.md`, or implement an automated unit test in `tests/test_customer.py` or a dedicated test verifying that all public symbols in `search_service.py` are exported identically by `search.py` and `__init__.py`.

---

## IK-06

**What:**
The repository lacks a `.gitignore` file, resulting in compiled Python bytecode (`__pycache__/*.pyc`) being tracked under git version control. Running tests modifies these tracked bytecode files on disk, creating phantom uncommitted changes.

**Evidence:**
- `Test-Path .gitignore` returned `False`.
- `git ls-files "*pycache*"` returned 25 compiled `.pyc` files actively tracked in the git index.
- In `results/before-agent-run.md`, `git status` repeatedly reported modified binary files:
  `modified: src/customer_search/__pycache__/search_service.cpython-314.pyc`
  `modified: tests/__pycache__/test_search_matching.cpython-314-pytest-9.1.1.pyc`.

**How was it discovered:**
Discovered when checking `git status` after executing `pytest`, where binary `.pyc` files appeared in `Changes not staged for commit` despite no intentional edits to compiled files.

**Risk:**
An agent attempting to commit changes using `git commit -a` or `git add .` will commit machine-specific compiled bytecode, polluting git history, creating cross-environment merge conflicts, and potentially masking clean working trees.

**Should this remain implicit?**
NO. Repository hygiene and ignore rules must be explicitly handled by git configuration rather than developer vigilance.

**Where should it become explicit?**
- `.gitignore` at the repository root.
- `AGENTS.md` (under Git Workflow / Working Tree Rules).

**Remediation:**
Add a standard root `.gitignore` ignoring `__pycache__/`, `*.pyc`, `.pytest_cache/`, and `.venv/`, untrack existing `.pyc` files from git (`git rm -r --cached __pycache__`), and specify in `AGENTS.md` that agents must verify `git status` only includes intended source and test files.
