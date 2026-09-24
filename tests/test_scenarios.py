"""Comprehensive automated tests covering test scenarios TS-01 through TS-13 (T-08).

Verifies all acceptance criteria and requirements from SPEC.md and REQUIREMENTS.md:
- FR-01, FR-02, FR-03, FR-04, FR-05, FR-06, FR-07, FR-08
- NFR-01, NFR-02, NFR-03
- AC-01 through AC-11
- TS-01 through TS-13
"""

import json
import time
from pathlib import Path

import pytest

from customer_search import (
    Customer,
    MSG_EMPTY_SEARCH,
    MSG_NO_CUSTOMERS_FOUND,
    SearchService,
    format_customer_display,
    main,
    run_search_cli,
)


def test_ts_01_exact_search_by_name():
    """TS-01 / AC-01 / FR-01: Search using an exact customer name."""
    output_lines: list[str] = []
    exit_code = run_search_cli(
        args=["Alice"],
        output_func=output_lines.append,
    )

    assert exit_code == 0
    assert any("Alice Smith" in line for line in output_lines)


def test_ts_02_search_by_surname():
    """TS-02 / AC-01 / FR-01: Search using a surname."""
    output_lines: list[str] = []
    exit_code = run_search_cli(
        args=["Miller"],
        output_func=output_lines.append,
    )

    assert exit_code == 0
    assert any("Frank Miller" in line for line in output_lines)


def test_ts_03_search_by_full_name():
    """TS-03 / AC-01 / FR-01: Search using a full name."""
    output_lines: list[str] = []
    exit_code = run_search_cli(
        args=["David Wilson"],
        output_func=output_lines.append,
    )

    assert exit_code == 0
    assert any("David Wilson" in line and "david.wilson@example.com" in line for line in output_lines)


def test_ts_04_search_by_email():
    """TS-04 / AC-02 / FR-01: Search using an email address."""
    output_lines: list[str] = []
    exit_code = run_search_cli(
        args=["charlie.brown@example.com"],
        output_func=output_lines.append,
    )

    assert exit_code == 0
    assert any("Charlie Brown" in line and "charlie.brown@example.com" in line for line in output_lines)


def test_ts_05_partial_matches():
    """TS-05 / AC-03 / FR-02: Search using part of a name or email."""
    output_lines: list[str] = []
    exit_code = run_search_cli(
        args=["jack"],
        output_func=output_lines.append,
    )

    assert exit_code == 0
    # "Jack Jackson" matches both first name "Jack" and surname "Jackson"
    assert any("Jack Jackson" in line for line in output_lines)


def test_ts_06_case_insensitive_searches():
    """TS-06 / AC-04 / FR-03: Search using uppercase and lowercase variations."""
    output_lower: list[str] = []
    output_upper: list[str] = []
    output_mixed: list[str] = []

    run_search_cli(args=["grace"], output_func=output_lower.append)
    run_search_cli(args=["GRACE"], output_func=output_upper.append)
    run_search_cli(args=["GrAcE"], output_func=output_mixed.append)

    assert output_lower == output_upper == output_mixed
    assert len(output_lower) == 1
    assert "Grace Taylor" in output_lower[0]


def test_ts_07_exact_matches_before_partial_matches():
    """TS-07 / AC-06 / FR-04: Exact matches appear before partial matches."""
    output_lines: list[str] = []
    run_search_cli(args=["John"], output_func=output_lines.append)

    # In default data:
    # John Doe is an exact match on first name
    # Bob Johnson is a partial match on surname
    assert len(output_lines) >= 2
    assert "John Doe" in output_lines[0]
    assert "Bob Johnson" in output_lines[1]


def test_ts_08_no_matching_customers():
    """TS-08 / AC-05 / FR-05: Search with no matching customers."""
    output_lines: list[str] = []
    exit_code = run_search_cli(
        args=["definitely_non_matching_search_term_12345"],
        output_func=output_lines.append,
    )

    assert exit_code == 0
    assert output_lines == [MSG_NO_CUSTOMERS_FOUND]


def test_ts_09_more_than_10_results_limited_to_10(tmp_path: Path):
    """TS-09 / AC-07 / FR-06: Search producing more than 10 results displays at most 10."""
    records = [
        {"name": f"User{i:02d}", "surname": "MatchingGroup", "email": f"user{i:02d}@example.com"}
        for i in range(18)
    ]
    data_file = tmp_path / "overflow_customers.json"
    data_file.write_text(json.dumps(records), encoding="utf-8")

    service = SearchService(data_path=data_file)
    output_lines: list[str] = []
    run_search_cli(
        args=["MatchingGroup"],
        service=service,
        output_func=output_lines.append,
    )

    assert len(output_lines) == 10


def test_ts_10_only_full_name_and_email_displayed():
    """TS-10 / AC-08 / FR-07: Search results display only full name and email."""
    output_lines: list[str] = []
    run_search_cli(args=["Emma"], output_func=output_lines.append)

    assert len(output_lines) == 1
    # Exactly full name, separator, email
    line = output_lines[0]
    assert line == "Emma Davis - emma.davis@example.com"
    parts = line.split(" - ")
    assert len(parts) == 2
    assert parts[0] == "Emma Davis"
    assert parts[1] == "emma.davis@example.com"


def test_ts_11_empty_or_whitespace_only_input():
    """TS-11 / AC-09 / FR-08: Empty or whitespace-only search input."""
    output_empty: list[str] = []
    exit_empty = run_search_cli(
        input_func=lambda _: "",
        output_func=output_empty.append,
    )
    assert exit_empty == 1
    assert output_empty == [MSG_EMPTY_SEARCH]

    output_ws: list[str] = []
    exit_ws = run_search_cli(
        input_func=lambda _: "   \t \n ",
        output_func=output_ws.append,
    )
    assert exit_ws == 1
    assert output_ws == [MSG_EMPTY_SEARCH]


def test_ts_12_execute_search_using_enter():
    """TS-12 / AC-10 / NFR-03: Execute a valid search by pressing Enter in CLI."""
    prompt_shown: list[str] = []
    output_lines: list[str] = []

    def user_types_and_presses_enter(prompt: str) -> str:
        prompt_shown.append(prompt)
        return "Ivy"

    exit_code = run_search_cli(
        input_func=user_types_and_presses_enter,
        output_func=output_lines.append,
    )

    assert exit_code == 0
    assert prompt_shown == ["Enter search term: "]
    assert len(output_lines) == 1
    assert "Ivy Thomas - ivy.thomas@example.com" in output_lines[0]


def test_ts_13_up_to_10000_customers_response_time(tmp_path: Path):
    """TS-13 / AC-11 / NFR-01 / NFR-02: Search up to 10,000 customers finishes in < 2 seconds without error."""
    # Generate 10,000 customers
    large_dataset = [
        {"name": f"First{i}", "surname": f"Last{i}", "email": f"email{i}@example.com"}
        for i in range(10_000)
    ]
    # Inject a specific target record near the end of the dataset
    large_dataset[9950] = {
        "name": "BenchmarkUser",
        "surname": "TargetSurname",
        "email": "benchmark@example.com",
    }

    data_file = tmp_path / "10k_dataset.json"
    data_file.write_text(json.dumps(large_dataset), encoding="utf-8")

    service = SearchService(data_path=data_file)
    output_lines: list[str] = []

    start = time.perf_counter()
    exit_code = run_search_cli(
        args=["BenchmarkUser"],
        service=service,
        output_func=output_lines.append,
    )
    elapsed = time.perf_counter() - start

    assert exit_code == 0
    assert elapsed < 2.0, f"Search took {elapsed:.3f}s, expected < 2.0s"
    assert len(output_lines) == 1
    assert "BenchmarkUser TargetSurname - benchmark@example.com" in output_lines[0]


def test_invalid_customer_data_graceful_handling(tmp_path: Path):
    """Verify invalid customer records do not produce an unhandled error (NFR-02, VR-04, EH-04)."""
    corrupt_dataset = [
        {"name": "GoodUser", "surname": "Surname", "email": "good@example.com"},
        {"bad_record": None},
        "corrupt_string_entry",
        {"name": "", "surname": "MissingFirst", "email": "missing@example.com"},
    ]
    data_file = tmp_path / "corrupted_records.json"
    data_file.write_text(json.dumps(corrupt_dataset), encoding="utf-8")

    service = SearchService(data_path=data_file)
    output_lines: list[str] = []
    exit_code = run_search_cli(
        args=["GoodUser"],
        service=service,
        output_func=output_lines.append,
    )

    assert exit_code == 0
    assert len(output_lines) == 1
    assert "GoodUser Surname - good@example.com" in output_lines[0]
