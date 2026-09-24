"""Customer search service module.

Implements search matching, match classification, result ordering, result limits,
input validation, and user message formatting.
Satisfies: FR-01, FR-02, FR-03, FR-04, FR-05, FR-06, FR-08,
           SR-01, SR-02, SR-03, SR-04, SR-05, SR-06, SR-07, SR-09, SR-11,
           VR-01, VR-02, VR-03, VR-04, EH-01, EH-02, EH-03, EH-04.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Sequence

from customer_search.customer import Customer
from customer_search.data_loader import load_customers

# Maximum number of customer results per search (FR-06, SR-07)
MAX_RESULTS: int = 10

# Standard messages defined by requirements and specification
MSG_EMPTY_SEARCH: str = "Please enter a search term"
MSG_NO_CUSTOMERS_FOUND: str = "No customers found"


class InvalidSearchTermError(ValueError):
    """Raised when search input is empty or contains only whitespace characters (FR-08, EH-01, EH-02)."""

    pass


class MatchType(Enum):
    """Classification of search matches."""

    EXACT = auto()
    PARTIAL = auto()


@dataclass(frozen=True)
class CustomerMatch:
    """Represents a matched customer and its match classification."""

    customer: Customer
    match_type: MatchType


@dataclass(frozen=True)
class SearchResult:
    """Represents the outcome of a search operation.

    Attributes:
        customers: List of matching customer records (up to MAX_RESULTS).
        message: Informational or validation message (e.g. 'No customers found',
            'Please enter a search term'), or None when matching customers exist.
        is_valid: True if input was valid and search could proceed; False otherwise.
    """

    customers: list[Customer] = field(default_factory=list)
    message: str | None = None
    is_valid: bool = True


def normalize_text(text: str) -> str:
    """Normalize text for case-insensitive comparison.

    Per SR-04, search comparison shall be case-insensitive and normalized.
    """
    return text.strip().lower()


def validate_search_term(query: str | None) -> str:
    """Validate search input before execution.

    Per VR-02, VR-03, EH-01, and EH-02:
    - Empty input is rejected.
    - Whitespace-only input is rejected.

    Args:
        query: The raw search input.

    Returns:
        The validated query string.

    Raises:
        InvalidSearchTermError: If query is None, empty, or whitespace-only.
    """
    if query is None or not query.strip():
        raise InvalidSearchTermError(MSG_EMPTY_SEARCH)
    return query


def customer_sort_key(customer: Customer) -> tuple[str, str, str]:
    """Provide a deterministic sort key for alphabetical customer ordering.

    Per SR-06, customers with the same match priority are sorted alphabetically.
    Sorts by name, then surname, then email address.
    """
    return (
        customer.name.strip().lower(),
        customer.surname.strip().lower(),
        customer.email.strip().lower(),
    )


def classify_match(customer: Customer, query: str) -> MatchType | None:
    """Classify the match type of a customer against a query.

    Evaluates the search term against:
    - name
    - surname
    - full name
    - email

    Args:
        customer: The customer record to evaluate.
        query: The search term entered by the user.

    Returns:
        MatchType.EXACT if the normalized query equals any normalized field.
        MatchType.PARTIAL if the normalized query is contained in any normalized field.
        None if no field matches.
    """
    normalized_query = normalize_text(query)
    if not normalized_query:
        return None

    searchable_fields = [
        customer.name.strip().lower(),
        customer.surname.strip().lower(),
        customer.full_name.strip().lower(),
        customer.email.strip().lower(),
    ]

    # SR-05: Exact match occurs when normalized search string is equal to at least one field
    if any(normalized_query == field for field in searchable_fields):
        return MatchType.EXACT

    # SR-03: Partial match occurs when normalized search string is contained in at least one field
    if any(normalized_query in field for field in searchable_fields):
        return MatchType.PARTIAL

    return None


class SearchService:
    """Service responsible for searching customer records."""

    def __init__(
        self,
        customers: Sequence[Customer] | None = None,
        data_path: str | Path | None = None,
    ) -> None:
        """Initialize SearchService with an optional customer list or data file path."""
        self._customers = list(customers) if customers is not None else None
        self._data_path = data_path

    def get_customers(self) -> list[Customer]:
        """Retrieve customers from provided sequence or load from the data loader."""
        if self._customers is not None:
            return self._customers
        return load_customers(self._data_path)

    def find_matches(self, query: str) -> list[CustomerMatch]:
        """Find and classify all matching customers for a query.

        Args:
            query: The search term.

        Returns:
            A list of CustomerMatch objects identifying customer and match type.
        """
        matches: list[CustomerMatch] = []
        for customer in self.get_customers():
            match_type = classify_match(customer, query)
            if match_type is not None:
                matches.append(CustomerMatch(customer=customer, match_type=match_type))
        return matches

    def get_exact_matches(self, query: str) -> list[Customer]:
        """Return all customers with exact matches for the query, sorted alphabetically."""
        exact = [m.customer for m in self.find_matches(query) if m.match_type == MatchType.EXACT]
        return sorted(exact, key=customer_sort_key)

    def get_partial_matches(self, query: str) -> list[Customer]:
        """Return all customers with partial matches for the query, sorted alphabetically."""
        partial = [m.customer for m in self.find_matches(query) if m.match_type == MatchType.PARTIAL]
        return sorted(partial, key=customer_sort_key)

    def search(self, query: str, limit: int = MAX_RESULTS) -> list[Customer]:
        """Search customers by query, applying ordering and result limit rules.

        Rules applied:
        - SR-06: Exact matches are displayed before partial matches.
        - SR-06: Customers with the same match priority are sorted alphabetically.
        - SR-07: Results are limited to a maximum of 10 customers (or specified limit).

        Args:
            query: The search term.
            limit: Maximum number of results to return (default: MAX_RESULTS = 10).

        Returns:
            A list of matching Customer records up to the limit.
        """
        exact_sorted = self.get_exact_matches(query)
        partial_sorted = self.get_partial_matches(query)

        ordered = exact_sorted + partial_sorted
        return ordered[:limit]

    def execute_search(self, query: str | None, limit: int = MAX_RESULTS) -> SearchResult:
        """Execute a customer search with input validation and message reporting (T-06).

        Per VR-02, VR-03, EH-01, EH-02, EH-03:
        1. Validates query input.
        2. If invalid (empty or whitespace-only), search is NOT executed, and
           message 'Please enter a search term' is returned with is_valid=False.
        3. If valid, searches customer data.
        4. If no customers match, message 'No customers found' is returned.
        5. If customers match, returns them with message=None.

        Args:
            query: The raw search input.
            limit: Maximum number of results to return.

        Returns:
            A SearchResult containing the customers, message, and validation status.
        """
        try:
            valid_query = validate_search_term(query)
        except InvalidSearchTermError:
            return SearchResult(
                customers=[],
                message=MSG_EMPTY_SEARCH,
                is_valid=False,
            )

        customers = self.search(valid_query, limit=limit)
        if not customers:
            return SearchResult(
                customers=[],
                message=MSG_NO_CUSTOMERS_FOUND,
                is_valid=True,
            )

        return SearchResult(
            customers=customers,
            message=None,
            is_valid=True,
        )


def search(
    query: str,
    customers: Sequence[Customer] | None = None,
    data_path: str | Path | None = None,
    limit: int = MAX_RESULTS,
) -> list[Customer]:
    """Convenience function to search customers with ordering and limit."""
    service = SearchService(customers=customers, data_path=data_path)
    return service.search(query, limit=limit)


def execute_search(
    query: str | None,
    customers: Sequence[Customer] | None = None,
    data_path: str | Path | None = None,
    limit: int = MAX_RESULTS,
) -> SearchResult:
    """Convenience function to execute a validated search."""
    service = SearchService(customers=customers, data_path=data_path)
    return service.execute_search(query, limit=limit)
