"""Unit tests for search input validation and error handling (T-06)."""

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from customer_search import (
    Customer,
    InvalidSearchTermError,
    MSG_EMPTY_SEARCH,
    MSG_NO_CUSTOMERS_FOUND,
    SearchResult,
    SearchService,
    execute_search,
    validate_search_term,
)


def test_validate_search_term_rejects_empty():
    """Verify empty input raises InvalidSearchTermError with standard message (VR-02, EH-01)."""
    with pytest.raises(InvalidSearchTermError) as exc_info:
        validate_search_term("")
    assert str(exc_info.value) == MSG_EMPTY_SEARCH

    with pytest.raises(InvalidSearchTermError) as exc_info:
        validate_search_term(None)
    assert str(exc_info.value) == MSG_EMPTY_SEARCH


def test_validate_search_term_rejects_whitespace_only():
    """Verify whitespace-only input raises InvalidSearchTermError (VR-03, EH-02)."""
    with pytest.raises(InvalidSearchTermError) as exc_info:
        validate_search_term("   ")
    assert str(exc_info.value) == MSG_EMPTY_SEARCH

    with pytest.raises(InvalidSearchTermError) as exc_info:
        validate_search_term(" \t \n ")
    assert str(exc_info.value) == MSG_EMPTY_SEARCH


def test_validate_search_term_accepts_valid_string():
    """Verify non-empty text passes validation (VR-01)."""
    assert validate_search_term("Alice") == "Alice"
    assert validate_search_term("  Bob  ") == "  Bob  "


def test_execute_search_with_empty_input():
    """Verify empty input returns validation message and is_valid=False (FR-08, AC-09, TS-11)."""
    service = SearchService(customers=[])
    result = service.execute_search("")

    assert result.is_valid is False
    assert result.message == MSG_EMPTY_SEARCH
    assert result.customers == []


def test_execute_search_with_whitespace_only_input():
    """Verify whitespace-only input returns validation message (FR-08, AC-09, TS-11)."""
    service = SearchService(customers=[])
    result = service.execute_search("     ")

    assert result.is_valid is False
    assert result.message == MSG_EMPTY_SEARCH
    assert result.customers == []


def test_search_not_executed_for_invalid_input():
    """Verify customer data is not accessed/loaded when input is invalid (T-06, EH-01, EH-02)."""
    service = SearchService(customers=None)
    service.get_customers = MagicMock(return_value=[])  # type: ignore[method-assign]

    # Run invalid searches
    service.execute_search("")
    service.execute_search("   ")
    service.execute_search(None)

    # get_customers must never have been called
    assert service.get_customers.call_count == 0


def test_execute_search_no_matching_customers():
    """Verify 'No customers found' is displayed when search has no matches (FR-05, SR-09, EH-03, AC-05, TS-08)."""
    customers = [
        Customer(name="Alice", surname="Smith", email="alice@example.com"),
    ]
    service = SearchService(customers=customers)
    result = service.execute_search("Zachary")

    assert result.is_valid is True
    assert result.message == MSG_NO_CUSTOMERS_FOUND
    assert result.customers == []


def test_execute_search_successful_matches():
    """Verify valid search with matches returns customers and no error message."""
    customers = [
        Customer(name="Alice", surname="Smith", email="alice@example.com"),
    ]
    service = SearchService(customers=customers)
    result = service.execute_search("Alice")

    assert result.is_valid is True
    assert result.message is None
    assert len(result.customers) == 1
    assert result.customers[0].name == "Alice"


def test_convenience_execute_search():
    """Verify module-level execute_search helper function."""
    customers = [Customer(name="Charlie", surname="Brown", email="charlie@example.com")]

    result_invalid = execute_search("  ", customers=customers)
    assert result_invalid.is_valid is False
    assert result_invalid.message == MSG_EMPTY_SEARCH

    result_none = execute_search("xyz", customers=customers)
    assert result_none.is_valid is True
    assert result_none.message == MSG_NO_CUSTOMERS_FOUND

    result_match = execute_search("Brown", customers=customers)
    assert result_match.is_valid is True
    assert result_match.message is None
    assert len(result_match.customers) == 1


def test_invalid_customer_data_does_not_cause_unhandled_error(tmp_path: Path):
    """Verify invalid customer data does not produce unhandled application errors (NFR-02, VR-04, EH-04)."""
    bad_data = [
        {"name": "Valid", "surname": "Customer", "email": "valid@example.com"},
        {"corrupt": True},
        12345,
        {"name": "Broken"},
    ]
    data_file = tmp_path / "corrupted_customers.json"
    data_file.write_text(json.dumps(bad_data), encoding="utf-8")

    service = SearchService(data_path=data_file)

    # Search for the valid customer
    result_valid = service.execute_search("Valid")
    assert result_valid.is_valid is True
    assert len(result_valid.customers) == 1
    assert result_valid.customers[0].name == "Valid"

    # Search for a customer that does not exist in the corrupted dataset
    result_missing = service.execute_search("NonExistent")
    assert result_missing.is_valid is True
    assert result_missing.message == MSG_NO_CUSTOMERS_FOUND
    assert result_missing.customers == []


def test_corrupt_json_file_does_not_cause_unhandled_error(tmp_path: Path):
    """Verify completely malformed JSON file does not crash search."""
    data_file = tmp_path / "malformed.json"
    data_file.write_text("{ unclosed json", encoding="utf-8")

    service = SearchService(data_path=data_file)
    result = service.execute_search("AnyTerm")

    assert result.is_valid is True
    assert result.message == MSG_NO_CUSTOMERS_FOUND
    assert result.customers == []
