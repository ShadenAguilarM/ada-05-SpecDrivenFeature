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
    MatchType,
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

    # Partial email match: "john" is present in Customer 2's email
    results = service.search("john", field="email")
    assert len(results) == 1
    assert results[0].name == "Alice"
    assert results[0].email == "john.worker@example.com"

    # Exact email match: full email address
    exact_results = service.search("john.worker@example.com", field="email")
    assert len(exact_results) == 1
    assert exact_results[0].name == "Alice"
    assert exact_results[0].email == "john.worker@example.com"


def test_filter_by_name_only(filter_customers: list[Customer]):
    """Verify field='name' returns only customers whose name matches the query (CR-01, AC-01, FR-01)."""
    service = SearchService(customers=filter_customers)

    # Exact name match
    results = service.search("john", field="name")
    assert len(results) == 1
    assert results[0].name == "John"
    assert results[0].surname == "Doe"

    # Partial name match: "joh"
    partial_results = service.search("joh", field="name")
    assert len(partial_results) == 1
    assert partial_results[0].name == "John"
    assert partial_results[0].surname == "Doe"


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

    # Exact full name match
    results = service.search("Elton John", field="full_name")
    assert len(results) == 1
    assert results[0].full_name == "Elton John"

    # Partial full name match
    partial_results = service.search("ton joh", field="full_name")
    assert len(partial_results) == 1
    assert partial_results[0].full_name == "Elton John"


def test_find_matches_with_field_filter(filter_customers: list[Customer]):
    """Verify find_matches restricts matching to specified field and returns correct MatchType (CR-01)."""
    service = SearchService(customers=filter_customers)

    # Email field: only Alice has 'john' in email (partial match)
    matches_email = service.find_matches("john", field="email")
    assert len(matches_email) == 1
    assert matches_email[0].customer.email == "john.worker@example.com"
    assert matches_email[0].match_type == MatchType.PARTIAL

    # Name field: only John has 'john' in first name (exact match)
    matches_name = service.find_matches("john", field="name")
    assert len(matches_name) == 1
    assert matches_name[0].customer.name == "John"
    assert matches_name[0].match_type == MatchType.EXACT

    # Surname field: Elton John (exact) and Robert Johnson (partial)
    matches_surname = service.find_matches("john", field="surname")
    assert len(matches_surname) == 2
    surname_matches_by_name = {m.customer.name: m for m in matches_surname}
    assert surname_matches_by_name["Elton"].match_type == MatchType.EXACT
    assert surname_matches_by_name["Robert"].match_type == MatchType.PARTIAL

    # Full name field: exact match on "Elton John"
    matches_fn_exact = service.find_matches("Elton John", field="full_name")
    assert len(matches_fn_exact) == 1
    assert matches_fn_exact[0].customer.name == "Elton"
    assert matches_fn_exact[0].match_type == MatchType.EXACT

    # Full name field: partial matches on "john"
    matches_fn_partial = service.find_matches("john", field="full_name")
    assert len(matches_fn_partial) == 3
    fn_matches_by_name = {m.customer.name: m for m in matches_fn_partial}
    assert fn_matches_by_name["John"].match_type == MatchType.PARTIAL
    assert fn_matches_by_name["Robert"].match_type == MatchType.PARTIAL
    assert fn_matches_by_name["Elton"].match_type == MatchType.PARTIAL

    # Empty query returns no matches and None for classify_match
    assert service.find_matches("", field="name") == []
    assert classify_match(filter_customers[0], "", field="name") is None


def test_get_exact_matches_with_field_filter(filter_customers: list[Customer]):
    """Verify get_exact_matches filters and sorts correctly when field is specified (CR-01)."""
    service = SearchService(customers=filter_customers)

    # Exact match on name
    exact_name = service.get_exact_matches("john", field="name")
    assert len(exact_name) == 1
    assert exact_name[0].name == "John"

    # Exact match on surname
    exact_surname = service.get_exact_matches("john", field="surname")
    assert len(exact_surname) == 1
    assert exact_surname[0].surname == "John"

    # Exact match on full_name
    exact_fn = service.get_exact_matches("elton john", field="full_name")
    assert len(exact_fn) == 1
    assert exact_fn[0].full_name == "Elton John"

    # Exact match on email
    exact_email = service.get_exact_matches("john.worker@example.com", field="email")
    assert len(exact_email) == 1
    assert exact_email[0].email == "john.worker@example.com"

    # Substring query does not return exact matches
    assert service.get_exact_matches("john", field="email") == []


def test_get_partial_matches_with_field_filter(filter_customers: list[Customer]):
    """Verify get_partial_matches filters and sorts correctly when field is specified (CR-01)."""
    service = SearchService(customers=filter_customers)

    # Partial match on email
    partial_email = service.get_partial_matches("john", field="email")
    assert len(partial_email) == 1
    assert partial_email[0].name == "Alice"

    # Partial match on surname (Elton is exact, Robert is partial)
    partial_surname = service.get_partial_matches("john", field="surname")
    assert len(partial_surname) == 1
    assert partial_surname[0].name == "Robert"

    # Partial match on full_name (sorted alphabetically by customer_sort_key: Elton John, John Doe, Robert Johnson)
    partial_fn = service.get_partial_matches("john", field="full_name")
    assert len(partial_fn) == 3
    assert [c.name for c in partial_fn] == ["Elton", "John", "Robert"]

    # Non-matching query returns empty
    assert service.get_partial_matches("xyz", field="name") == []


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
