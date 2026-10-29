"""Unit tests for optional field-filtered customer search (CR-01).

Covers requirements and acceptance criteria:
- FR-01: Search customers by name, surname, full name, or email address.
- FR-02: Partial matching on customer fields.
- AC-01: Name search.
- AC-02: Email search.
- AC-03: Substring search across searchable fields.
- CR-01: Optional field filter parameter with backward compatibility and validation.
"""

import pytest

from customer_search import (
    MSG_EMPTY_SEARCH,
    MSG_NO_CUSTOMERS_FOUND,
    VALID_SEARCH_FIELDS,
    Customer,
    SearchService,
    classify_match,
    execute_search,
    search,
)


@pytest.fixture
def filter_customers() -> list[Customer]:
    """Sample customers with overlapping values across different fields."""
    return [
        # John matches on name
        Customer(name="John", surname="Doe", email="jdoe@example.com"),
        # Alice matches on email containing 'john'
        Customer(name="Alice", surname="Smith", email="john.worker@example.com"),
        # Robert matches on surname containing 'john'
        Customer(name="Robert", surname="Johnson", email="robert@example.com"),
        # Elton matches on full name
        Customer(name="Elton", surname="John", email="elton@music.org"),
    ]


def test_filter_by_email_only(filter_customers: list[Customer]):
    """Verify field='email' returns only customers whose email matches the query (CR-01, AC-02, FR-01)."""
    service = SearchService(customers=filter_customers)

    # "john" is present in Customer 1's name, Customer 2's email, Customer 3's surname, Customer 4's surname/full_name
    results = service.search("john", field="email")

    assert len(results) == 1
    assert results[0].name == "Alice"
    assert results[0].email == "john.worker@example.com"


def test_filter_by_name_only(filter_customers: list[Customer]):
    """Verify field='name' returns only customers whose name matches the query (CR-01, AC-01, FR-01)."""
    service = SearchService(customers=filter_customers)

    results = service.search("john", field="name")

    assert len(results) == 1
    assert results[0].name == "John"
    assert results[0].surname == "Doe"


def test_filter_by_surname_only(filter_customers: list[Customer]):
    """Verify field='surname' returns only customers whose surname matches the query (CR-01, FR-01)."""
    service = SearchService(customers=filter_customers)

    results = service.search("john", field="surname")

    # Elton John (exact surname match) and Robert Johnson (partial surname match)
    assert len(results) == 2
    assert results[0].surname == "John"  # Exact match ordered first
    assert results[1].surname == "Johnson"  # Partial match ordered second


def test_filter_by_full_name_only(filter_customers: list[Customer]):
    """Verify field='full_name' returns only customers whose full name matches the query (CR-01, FR-01)."""
    service = SearchService(customers=filter_customers)

    results = service.search("Elton John", field="full_name")

    assert len(results) == 1
    assert results[0].full_name == "Elton John"


def test_filter_none_or_omitted_preserves_default_behavior(filter_customers: list[Customer]):
    """Verify omitting field or passing field=None evaluates across all searchable attributes (CR-01)."""
    service = SearchService(customers=filter_customers)

    results_omitted = service.search("john")
    results_none = service.search("john", field=None)

    assert results_omitted == results_none
    # Matches all 4 customers across name, email, surname, full name
    assert len(results_omitted) == 4


def test_unsupported_field_raises_value_error(filter_customers: list[Customer]):
    """Verify providing an unsupported field name raises a ValueError (CR-01)."""
    service = SearchService(customers=filter_customers)

    for invalid_field in ["phone", "address", "age", "NAME", ""]:
        with pytest.raises(ValueError, match="Unsupported search field"):
            service.search("john", field=invalid_field)

        with pytest.raises(ValueError, match="Unsupported search field"):
            service.find_matches("john", field=invalid_field)

        with pytest.raises(ValueError, match="Unsupported search field"):
            service.execute_search("john", field=invalid_field)

        with pytest.raises(ValueError, match="Unsupported search field"):
            classify_match(filter_customers[0], "john", field=invalid_field)


def test_execute_search_with_field_filter(filter_customers: list[Customer]):
    """Verify execute_search respects the field filter and returns appropriate SearchResult (CR-01)."""
    service = SearchService(customers=filter_customers)

    # Valid search with matches
    result = service.execute_search("john", field="email")
    assert result.is_valid is True
    assert result.message is None
    assert len(result.customers) == 1
    assert result.customers[0].email == "john.worker@example.com"

    # Valid search with no matches in specified field
    result_none = service.execute_search("smith", field="email")
    assert result_none.is_valid is True
    assert result_none.message == MSG_NO_CUSTOMERS_FOUND
    assert result_none.customers == []

    # Invalid input (empty query) rejects search before field filtering
    result_empty = service.execute_search("", field="email")
    assert result_empty.is_valid is False
    assert result_empty.message == MSG_EMPTY_SEARCH
    assert result_empty.customers == []


def test_convenience_functions_support_field_filter(filter_customers: list[Customer]):
    """Verify module-level search and execute_search accept field parameter (CR-01)."""
    results = search("john", customers=filter_customers, field="name")
    assert len(results) == 1
    assert results[0].name == "John"

    result_exec = execute_search("john", customers=filter_customers, field="name")
    assert result_exec.is_valid is True
    assert len(result_exec.customers) == 1
    assert result_exec.customers[0].name == "John"


def test_valid_search_fields_constant():
    """Verify VALID_SEARCH_FIELDS contains the expected customer attributes (CR-01)."""
    assert VALID_SEARCH_FIELDS == frozenset({"name", "surname", "full_name", "email"})
