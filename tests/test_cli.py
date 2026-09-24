"""Unit tests for the Command-Line Interface (T-07)."""

import pytest

from customer_search import (
    Customer,
    MSG_EMPTY_SEARCH,
    MSG_NO_CUSTOMERS_FOUND,
    SearchService,
    format_customer_display,
    format_search_results,
    main,
    run_search_cli,
)


@pytest.fixture
def mock_service() -> SearchService:
    """Fixture providing a SearchService with sample data for CLI testing."""
    customers = [
        Customer(name="John", surname="Doe", email="john.doe@example.com"),
        Customer(name="Jane", surname="Doe", email="jane.doe@example.com"),
        Customer(name="Alice", surname="Smith", email="alice.smith@example.com"),
    ]
    return SearchService(customers=customers)


def test_cli_interactive_search_success(mock_service: SearchService):
    """Verify entering a valid search term and pressing Enter executes search (NFR-03, SR-10, AC-10, TS-12)."""
    prompt_received: list[str] = []
    output_lines: list[str] = []

    def mock_input(prompt: str) -> str:
        prompt_received.append(prompt)
        return "John"  # User enters 'John' and presses Enter

    exit_code = run_search_cli(
        service=mock_service,
        input_func=mock_input,
        output_func=output_lines.append,
    )

    assert exit_code == 0
    assert prompt_received == ["Enter search term: "]
    assert len(output_lines) == 1
    assert output_lines[0] == "John Doe - john.doe@example.com"


def test_cli_displays_only_full_name_and_email(mock_service: SearchService):
    """Verify search results display only each customer's full name and email (FR-07, SR-08, AC-08, TS-10)."""
    output_lines: list[str] = []

    # Searching "Doe" matches John Doe and Jane Doe
    run_search_cli(
        service=mock_service,
        input_func=lambda _: "Doe",
        output_func=output_lines.append,
    )

    assert len(output_lines) == 2
    # Verify exact format: "<full_name> - <email>" with nothing else
    for line in output_lines:
        parts = line.split(" - ")
        assert len(parts) == 2
        full_name, email = parts
        assert "@" in email
        assert full_name in ["Jane Doe", "John Doe"]


def test_format_customer_display():
    """Unit test for format_customer_display function (SR-08)."""
    customer = Customer(name="Ada", surname="Lovelace", email="ada@example.com")
    formatted = format_customer_display(customer)
    assert formatted == "Ada Lovelace - ada@example.com"


def test_cli_empty_input_displays_validation_message(mock_service: SearchService):
    """Verify empty input displays 'Please enter a search term' (FR-08, SR-11, AC-09, TS-11)."""
    output_lines: list[str] = []

    exit_code = run_search_cli(
        service=mock_service,
        input_func=lambda _: "",
        output_func=output_lines.append,
    )

    assert exit_code == 1
    assert output_lines == [MSG_EMPTY_SEARCH]


def test_cli_whitespace_only_input_displays_validation_message(mock_service: SearchService):
    """Verify whitespace-only input displays 'Please enter a search term' (FR-08, SR-11, AC-09, TS-11)."""
    output_lines: list[str] = []

    exit_code = run_search_cli(
        service=mock_service,
        input_func=lambda _: "   \t  ",
        output_func=output_lines.append,
    )

    assert exit_code == 1
    assert output_lines == [MSG_EMPTY_SEARCH]


def test_cli_no_matching_customers_displays_message(mock_service: SearchService):
    """Verify search with no matches displays 'No customers found' (FR-05, SR-09, AC-05, TS-08)."""
    output_lines: list[str] = []

    exit_code = run_search_cli(
        service=mock_service,
        input_func=lambda _: "UnknownPerson",
        output_func=output_lines.append,
    )

    assert exit_code == 0
    assert output_lines == [MSG_NO_CUSTOMERS_FOUND]


def test_cli_argument_mode(mock_service: SearchService):
    """Verify CLI accepts query as command-line arguments without prompting."""
    output_lines: list[str] = []

    exit_code = run_search_cli(
        args=["Alice"],
        service=mock_service,
        input_func=lambda _: pytest.fail("input_func should not be called when args provided"),
        output_func=output_lines.append,
    )

    assert exit_code == 0
    assert output_lines == ["Alice Smith - alice.smith@example.com"]


def test_cli_eof_handling(mock_service: SearchService):
    """Verify EOF (e.g. Ctrl+D) is handled gracefully without exception."""
    def raise_eof(_: str) -> str:
        raise EOFError()

    exit_code = run_search_cli(
        service=mock_service,
        input_func=raise_eof,
        output_func=lambda _: None,
    )
    assert exit_code == 0


def test_main_entry_point(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]):
    """Integration test for main() entry point with command-line arguments."""
    exit_code = main(["Alice"])
    assert exit_code == 0

    captured = capsys.readouterr()
    assert "Alice Smith - alice.smith@example.com" in captured.out
