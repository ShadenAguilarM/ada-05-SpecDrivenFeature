"""Unit tests for search result ordering and limit (T-05)."""

import pytest

from customer_search import Customer, MAX_RESULTS, SearchService, customer_sort_key, search


def test_exact_matches_before_partial_matches():
    """Verify exact matches appear before partial matches (FR-04, SR-06, AC-06, TS-07)."""
    customers = [
        # Partial match on "John" (surname contains "john")
        Customer(name="Bob", surname="Johnson", email="bob.j@example.com"),
        # Partial match on "John" (name contains "john")
        Customer(name="Johnny", surname="Depp", email="johnny@movies.com"),
        # Exact match on "John" (name == "john")
        Customer(name="John", surname="Doe", email="john.doe@example.com"),
        # Partial match on "John" (surname contains "john")
        Customer(name="Alice", surname="Johnson", email="alice.j@example.com"),
    ]

    service = SearchService(customers=customers)
    results = service.search("John")

    assert len(results) == 4
    # The first result must be the exact match: John Doe
    assert results[0].name == "John"
    assert results[0].surname == "Doe"

    # Following results must be partial matches, sorted alphabetically
    assert results[1].name == "Alice" and results[1].surname == "Johnson"
    assert results[2].name == "Bob" and results[2].surname == "Johnson"
    assert results[3].name == "Johnny" and results[3].surname == "Depp"


def test_alphabetical_sorting_for_exact_matches():
    """Verify customers with equal exact match priority are sorted alphabetically (SR-06)."""
    customers = [
        Customer(name="Zach", surname="Smith", email="zach@example.com"),
        Customer(name="Alice", surname="Smith", email="alice@example.com"),
        Customer(name="Brian", surname="Smith", email="brian@example.com"),
    ]

    service = SearchService(customers=customers)
    results = service.search("Smith")

    assert len(results) == 3
    assert [c.name for c in results] == ["Alice", "Brian", "Zach"]


def test_alphabetical_sorting_for_partial_matches():
    """Verify customers with equal partial match priority are sorted alphabetically (SR-06)."""
    customers = [
        Customer(name="David", surname="Wilson", email="david@example.com"),
        Customer(name="Charles", surname="Wilson", email="charles@example.com"),
        Customer(name="Bob", surname="Wilson", email="bob@example.com"),
    ]

    service = SearchService(customers=customers)
    # Searching substring "ils" matches all Wilson customers partially
    results = service.search("ils")

    assert len(results) == 3
    assert [c.name for c in results] == ["Bob", "Charles", "David"]


def test_alphabetical_sorting_tiebreak_by_surname_and_email():
    """Verify deterministic ordering when first names or full names match."""
    customers = [
        Customer(name="John", surname="Williams", email="john.w@example.com"),
        Customer(name="John", surname="Adams", email="john.a@example.com"),
        Customer(name="John", surname="Adams", email="a.john@example.com"),
    ]

    service = SearchService(customers=customers)
    results = service.search("John")

    assert len(results) == 3
    # Same first name 'John', sorted by surname ('Adams' before 'Williams')
    # Within 'Adams', sorted by email ('a.john@example.com' before 'john.a@example.com')
    assert results[0] == Customer(name="John", surname="Adams", email="a.john@example.com")
    assert results[1] == Customer(name="John", surname="Adams", email="john.a@example.com")
    assert results[2] == Customer(name="John", surname="Williams", email="john.w@example.com")


def test_result_limit_maximum_10():
    """Verify search returns at most 10 results when more than 10 match (FR-06, SR-07, AC-07, TS-09)."""
    # Create 25 matching customers
    customers = [
        Customer(name=f"Customer{i:02d}", surname="Test", email=f"user{i:02d}@example.com")
        for i in range(25)
    ]

    service = SearchService(customers=customers)
    results = service.search("Test")

    assert MAX_RESULTS == 10
    assert len(results) == 10
    # Verify the 10 results returned are the first 10 alphabetically
    expected_names = [f"Customer{i:02d}" for i in range(10)]
    assert [c.name for c in results] == expected_names


def test_result_limit_with_exact_and_partial_overflow():
    """Verify that exact matches are prioritized within the 10-result limit."""
    exact_matches = [
        Customer(name=f"Exact{i:02d}", surname="Target", email=f"exact{i:02d}@example.com")
        for i in range(7)
    ]
    partial_matches = [
        Customer(name=f"Partial{i:02d}", surname="SubTarget", email=f"partial{i:02d}@example.com")
        for i in range(8)
    ]

    # Total 15 matches (7 exact, 8 partial)
    customers = partial_matches + exact_matches
    service = SearchService(customers=customers)

    results = service.search("Target")
    assert len(results) == 10

    # First 7 must be all 7 exact matches (sorted alphabetically)
    for i in range(7):
        assert results[i].name == f"Exact{i:02d}"

    # Remaining 3 must be the first 3 partial matches (sorted alphabetically)
    for i in range(3):
        assert results[7 + i].name == f"Partial{i:02d}"


def test_result_limit_not_applied_when_under_limit():
    """Verify all results are returned when matching count is less than 10."""
    customers = [
        Customer(name="Anna", surname="Taylor", email="anna@example.com"),
        Customer(name="Ben", surname="Taylor", email="ben@example.com"),
    ]

    service = SearchService(customers=customers)
    results = service.search("Taylor")

    assert len(results) == 2


def test_customer_sort_key_case_insensitivity():
    """Verify sort key treats uppercase and lowercase identically."""
    c1 = Customer(name="alice", surname="SMITH", email="A@example.com")
    c2 = Customer(name="ALICE", surname="smith", email="a@example.com")
    assert customer_sort_key(c1) == customer_sort_key(c2)
