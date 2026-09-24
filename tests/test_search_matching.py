"""Unit tests for customer search matching (T-04)."""

import pytest

from customer_search import (
    Customer,
    CustomerMatch,
    MatchType,
    SearchService,
    classify_match,
    search,
)


@pytest.fixture
def sample_customers() -> list[Customer]:
    """Fixture providing a standard list of customers for testing matching rules."""
    return [
        Customer(name="Alice", surname="Smith", email="alice.smith@example.com"),
        Customer(name="Bob", surname="Johnson", email="bob.j@example.com"),
        Customer(name="John", surname="Doe", email="john.doe@example.com"),
        Customer(name="Johnny", surname="Depp", email="johnny.depp@movies.com"),
        Customer(name="Mary-Jane", surname="Watson", email="mj.watson@dailybugle.com"),
    ]


def test_exact_search_by_name(sample_customers: list[Customer]):
    """Verify exact search by customer name (FR-01, SR-05, TS-01)."""
    service = SearchService(customers=sample_customers)
    matches = service.find_matches("Alice")

    assert len(matches) == 1
    assert matches[0].customer.name == "Alice"
    assert matches[0].match_type == MatchType.EXACT


def test_exact_search_by_surname(sample_customers: list[Customer]):
    """Verify exact search by customer surname (FR-01, SR-05, TS-02)."""
    service = SearchService(customers=sample_customers)
    matches = service.find_matches("Smith")

    assert len(matches) == 1
    assert matches[0].customer.surname == "Smith"
    assert matches[0].match_type == MatchType.EXACT


def test_exact_search_by_full_name(sample_customers: list[Customer]):
    """Verify exact search by customer full name (FR-01, SR-02, SR-05, TS-03)."""
    service = SearchService(customers=sample_customers)
    matches = service.find_matches("Alice Smith")

    assert len(matches) == 1
    assert matches[0].customer.full_name == "Alice Smith"
    assert matches[0].match_type == MatchType.EXACT


def test_exact_search_by_email(sample_customers: list[Customer]):
    """Verify exact search by customer email address (FR-01, SR-05, TS-04)."""
    service = SearchService(customers=sample_customers)
    matches = service.find_matches("alice.smith@example.com")

    assert len(matches) == 1
    assert matches[0].customer.email == "alice.smith@example.com"
    assert matches[0].match_type == MatchType.EXACT


def test_partial_search_by_name(sample_customers: list[Customer]):
    """Verify partial search matches customer name substring (FR-02, SR-03, TS-05)."""
    service = SearchService(customers=sample_customers)
    matches = service.find_matches("lic")

    assert len(matches) == 1
    assert matches[0].customer.name == "Alice"
    assert matches[0].match_type == MatchType.PARTIAL


def test_partial_search_by_surname(sample_customers: list[Customer]):
    """Verify partial search matches customer surname substring (FR-02, SR-03, TS-05)."""
    service = SearchService(customers=sample_customers)
    matches = service.find_matches("mit")

    assert len(matches) == 1
    assert matches[0].customer.surname == "Smith"
    assert matches[0].match_type == MatchType.PARTIAL


def test_partial_search_by_full_name(sample_customers: list[Customer]):
    """Verify partial search matches customer full name substring (FR-02, SR-03, TS-05)."""
    service = SearchService(customers=sample_customers)
    matches = service.find_matches("ce Sm")

    assert len(matches) == 1
    assert matches[0].customer.full_name == "Alice Smith"
    assert matches[0].match_type == MatchType.PARTIAL


def test_partial_search_by_email(sample_customers: list[Customer]):
    """Verify partial search matches customer email substring (FR-02, SR-03, TS-05)."""
    service = SearchService(customers=sample_customers)
    matches = service.find_matches("movies.com")

    assert len(matches) == 1
    assert matches[0].customer.name == "Johnny"
    assert matches[0].match_type == MatchType.PARTIAL


def test_case_insensitive_search(sample_customers: list[Customer]):
    """Verify searches with different casing produce the same results (FR-03, SR-04, TS-06)."""
    service = SearchService(customers=sample_customers)

    results_lower = service.search("alice")
    results_upper = service.search("ALICE")
    results_mixed = service.search("AlIcE")

    assert results_lower == results_upper == results_mixed
    assert len(results_lower) == 1
    assert results_lower[0].name == "Alice"


def test_classify_exact_and_partial_matches_separately(sample_customers: list[Customer]):
    """Verify exact matches are distinguished from partial matches (FR-04, SR-05, SR-03)."""
    service = SearchService(customers=sample_customers)

    # "John" is an exact match for "John Doe" (name field)
    # and a partial match for "Johnny Depp" (name) and "Bob Johnson" (surname)
    matches = service.find_matches("John")
    assert len(matches) == 3

    exact_matches = service.get_exact_matches("John")
    partial_matches = service.get_partial_matches("John")

    assert len(exact_matches) == 1
    assert exact_matches[0].name == "John"

    assert len(partial_matches) == 2
    assert {c.name for c in partial_matches} == {"Bob", "Johnny"}


def test_no_matches_returns_empty(sample_customers: list[Customer]):
    """Verify query with no matching customer returns empty list."""
    service = SearchService(customers=sample_customers)
    matches = service.find_matches("nonexistent_customer")
    assert matches == []
    assert service.search("nonexistent_customer") == []


def test_empty_or_whitespace_query_returns_empty(sample_customers: list[Customer]):
    """Verify empty or whitespace-only query returns no matches."""
    service = SearchService(customers=sample_customers)
    assert service.find_matches("") == []
    assert service.find_matches("   ") == []


def test_classify_match_function():
    """Unit test for classify_match function directly."""
    customer = Customer(name="Ada", surname="Lovelace", email="ada@example.com")

    assert classify_match(customer, "Ada") == MatchType.EXACT
    assert classify_match(customer, "Lovelace") == MatchType.EXACT
    assert classify_match(customer, "Ada Lovelace") == MatchType.EXACT
    assert classify_match(customer, "ada@example.com") == MatchType.EXACT

    assert classify_match(customer, "ad") == MatchType.PARTIAL
    assert classify_match(customer, "love") == MatchType.PARTIAL
    assert classify_match(customer, "example") == MatchType.PARTIAL

    assert classify_match(customer, "Charles") is None
