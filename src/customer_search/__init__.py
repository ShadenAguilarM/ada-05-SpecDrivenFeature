"""Customer Search Package."""

from customer_search.cli import format_customer_display, format_search_results, main, run_search_cli
from customer_search.customer import Customer
from customer_search.data_loader import load_customers
from customer_search.search_service import (
    MAX_RESULTS,
    MSG_EMPTY_SEARCH,
    MSG_NO_CUSTOMERS_FOUND,
    CustomerMatch,
    InvalidSearchTermError,
    MatchType,
    SearchResult,
    SearchService,
    classify_match,
    customer_sort_key,
    execute_search,
    search,
    validate_search_term,
)

__all__ = [
    "MAX_RESULTS",
    "MSG_EMPTY_SEARCH",
    "MSG_NO_CUSTOMERS_FOUND",
    "Customer",
    "CustomerMatch",
    "InvalidSearchTermError",
    "MatchType",
    "SearchResult",
    "SearchService",
    "classify_match",
    "customer_sort_key",
    "execute_search",
    "format_customer_display",
    "format_search_results",
    "load_customers",
    "main",
    "run_search_cli",
    "search",
    "validate_search_term",
]
