# Customer Search — CLI Application

A lightweight, spec-driven command-line Customer Search application written in Python 3.11+.

This application allows users to search customer records by first name, surname, full name, or email address with exact-match prioritization, alphabetical ordering, and error resilience using a local read-only JSON data source.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Execution](#execution)
  - [Interactive Mode](#1-interactive-mode)
  - [Argument Mode](#2-argument-mode)
  - [Behavior and Display Rules](#behavior-and-display-rules)
- [Testing](#testing)
  - [Running Tests](#running-tests)
  - [Test Suite Breakdown](#test-suite-breakdown)
- [Traceability & Documentation](#traceability--documentation)

---

## Features

- **Multi-Field Search**: Searches across customer `name`, `surname`, derived `full_name`, and `email` (**FR-01**).
- **Exact & Partial Matching**: Supports partial substring searches while correctly distinguishing and prioritizing exact matches (**FR-02**, **FR-04**).
- **Case-Insensitive**: Evaluates search terms without distinguishing character casing (**FR-03**).
- **Deterministic Ordering**: Displays exact matches first, followed by partial matches, sorting results of equal priority alphabetically (**FR-04**, **SR-06**).
- **Result Limit**: Displays a maximum of 10 customers per search (**FR-06**, **SR-07**).
- **Clean Display**: Outputs strictly each customer's full name and email address (**FR-07**, **SR-08**).
- **Input Validation**: Rejects empty or whitespace-only input displaying `"Please enter a search term"` without executing the search (**FR-08**).
- **Zero Database Dependency**: Uses a local, read-only JSON data source (`data/customers.json`) (**C-02**, **A-01**).
- **High Performance**: Evaluates and searches 10,000 customer records in ~0.08 seconds (well under the 2-second requirement) (**NFR-01**, **NFR-02**).

---

## Project Structure

```text
ada-05-SpecDrivenFeature/
├── data/
│   └── customers.json           # Local JSON customer dataset (read-only)
├── src/
│   └── customer_search/
│       ├── __init__.py          # Package exports
│       ├── __main__.py          # Package executable entry point
│       ├── cli.py               # Command-line interface logic
│       ├── customer.py          # Customer domain model dataclass
│       ├── data_loader.py       # JSON loader, validation, and error resilience
│       ├── loader.py            # Loader alias module
│       ├── models.py            # Model alias module
│       ├── search.py            # Search alias module
│       └── search_service.py    # Search matching, ordering, and limit engine
├── tests/
│   ├── __init__.py
│   ├── test_cli.py              # CLI interaction and formatting tests
│   ├── test_customer.py         # Customer domain model unit tests
│   ├── test_data_loader.py      # JSON data loader and validation tests
│   ├── test_ordering_and_limit.py # Priority ordering and limit tests
│   ├── test_scenarios.py        # End-to-end acceptance tests (TS-01 - TS-13)
│   ├── test_search_matching.py  # Matching and case-insensitivity tests
│   ├── test_setup.py            # Python environment verification
│   └── test_validation_and_errors.py # Input validation and error handling tests
├── pyproject.toml               # Project build configuration and pytest options
├── AGENTS.md                    # Project development instructions and constraints
├── ARCHITECTURE.md              # Architecture and component design document
├── REQUIREMENTS.md              # Functional and non-functional requirements
├── SPEC.md                      # Feature specifications and acceptance criteria
└── TASKS.md                     # Incremental task breakdown (T-01 to T-09)
```

---

## Requirements

- **Python**: Version `3.11` or higher (verified on Python `3.14`).
- **Dependencies**: `pytest >= 8.0` (standard library only for application runtime; no external dependencies or paid APIs).

---

## Installation

### 1. Navigate to the project directory

Open a terminal or PowerShell prompt and navigate to the project directory:

```bash
cd "C:\Users\ashle\Documents\ADA 05 IA\ada-05-SpecDrivenFeature"
```

### 2. (Optional) Set up a Virtual Environment

It is recommended to use a virtual environment:

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install testing dependencies

Install `pytest` if not already installed in your Python environment:

```bash
pip install pytest
```

*(Optional)* Install the package in editable mode:
```bash
pip install -e .
```

---

## Execution

The CLI application can be run interactively or by passing the search query as arguments.

### 1. Interactive Mode

Run the CLI directly:

**Using script execution:**
```powershell
python src/customer_search/cli.py
```

**Or using module execution:**
```powershell
python -m customer_search
```
*(Note: If running as a module without installing the package, set `PYTHONPATH=src`)*

**Interactive Flow:**
```text
Enter search term: John
John Doe - john.doe@example.com
Bob Johnson - bob.johnson@example.com
```

The user executes the search by pressing `Enter` (**NFR-03**, **SR-10**).

---

### 2. Argument Mode

You can also pass the search term directly on the command line:

```powershell
python src/customer_search/cli.py "Alice"
```

**Output:**
```text
Alice Smith - alice.smith@example.com
```

#### Additional Examples:

- **Search by Surname:**
  ```powershell
  python src/customer_search/cli.py "Miller"
  ```
  *Output:*
  ```text
  Frank Miller - frank.miller@example.com
  ```

- **Search by Full Name:**
  ```powershell
  python src/customer_search/cli.py "David Wilson"
  ```
  *Output:*
  ```text
  David Wilson - david.wilson@example.com
  ```

- **Search by Email:**
  ```powershell
  python src/customer_search/cli.py "charlie.brown@example.com"
  ```
  *Output:*
  ```text
  Charlie Brown - charlie.brown@example.com
  ```

- **Partial Substring Match:**
  ```powershell
  python src/customer_search/cli.py "son"
  ```
  *Output (exact matches before partial, sorted alphabetically):*
  ```text
  Bob Johnson - bob.johnson@example.com
  David Wilson - david.wilson@example.com
  Henry Anderson - henry.anderson@example.com
  Jack Jackson - jack.jackson@example.com
  ```

---

### Behavior and Display Rules

| Scenario | Input | Displayed Output |
|---|---|---|
| **Matching records** | `"John"` | `<full_name> - <email>` (e.g. `John Doe - john.doe@example.com`) |
| **No matches** | `"UnknownPerson"` | `No customers found` |
| **Empty input** | `""` | `Please enter a search term` |
| **Whitespace-only** | `"   "` | `Please enter a search term` |

---

## Testing

The project includes a comprehensive automated test suite with **73 unit and integration tests** built using `pytest`.

### Running Tests

To run the complete test suite, navigate to the `ada-05-SpecDrivenFeature` directory and run:

```powershell
pytest
```

To run with verbose output displaying every test name:

```powershell
pytest -v
```

### Test Suite Breakdown

| Test File | Covered Scope | Requirement / Task |
|---|---|---|
| [`tests/test_setup.py`](file:///C:/Users/ashle/Documents/ADA%2005%20IA/ada-05-SpecDrivenFeature/tests/test_setup.py) | Python 3.11+ version verification | **C-01**, **T-01** |
| [`tests/test_customer.py`](file:///C:/Users/ashle/Documents/ADA%2005%20IA/ada-05-SpecDrivenFeature/tests/test_customer.py) | Customer model, attributes, full name derivation, immutability | **FR-01**, **FR-07**, **T-02** |
| [`tests/test_data_loader.py`](file:///C:/Users/ashle/Documents/ADA%2005%20IA/ada-05-SpecDrivenFeature/tests/test_data_loader.py) | JSON parsing, record validation, read-only checks, 10k customer benchmark | **A-01**, **NFR-01**, **NFR-02**, **C-02**, **T-03** |
| [`tests/test_search_matching.py`](file:///C:/Users/ashle/Documents/ADA%2005%20IA/ada-05-SpecDrivenFeature/tests/test_search_matching.py) | Search fields, substring matching, case-insensitivity, exact vs partial classification | **FR-01**, **FR-02**, **FR-03**, **FR-04**, **T-04** |
| [`tests/test_ordering_and_limit.py`](file:///C:/Users/ashle/Documents/ADA%2005%20IA/ada-05-SpecDrivenFeature/tests/test_ordering_and_limit.py) | Exact-before-partial matching, alphabetical tie-breaking, max 10 result limit | **FR-04**, **FR-06**, **T-05** |
| [`tests/test_validation_and_errors.py`](file:///C:/Users/ashle/Documents/ADA%2005%20IA/ada-05-SpecDrivenFeature/tests/test_validation_and_errors.py) | Empty/whitespace validation, missing/corrupt data resilience | **FR-05**, **FR-08**, **NFR-02**, **T-06** |
| [`tests/test_cli.py`](file:///C:/Users/ashle/Documents/ADA%2005%20IA/ada-05-SpecDrivenFeature/tests/test_cli.py) | Interactive CLI loop, Enter key handling, output formatting, argument mode | **FR-07**, **NFR-03**, **T-07** |
| [`tests/test_scenarios.py`](file:///C:/Users/ashle/Documents/ADA%2005%20IA/ada-05-SpecDrivenFeature/tests/test_scenarios.py) | End-to-end acceptance tests covering scenarios **TS-01** through **TS-13** | **AC-01** - **AC-11**, **T-08**, **T-09** |

---

## Traceability & Documentation

- **Traceability Matrix**: Detailed requirement-to-test mapping is available in [`docs/traceability.md`](file:///C:/Users/ashle/Documents/ADA%2005%20IA/ada-05-SpecDrivenFeature/docs/traceability.md).
- **Execution Report**: Full task completion and benchmark metrics are available in [`results/agent-report.md`](file:///C:/Users/ashle/Documents/ADA%2005%20IA/ada-05-SpecDrivenFeature/results/agent-report.md).
