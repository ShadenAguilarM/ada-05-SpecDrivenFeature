"""Customer Search Package."""

from customer_search.cli import format_customer_display, format_search_results, main, run_search_cli
from customer_search.customer import Customer
from customer_search.data_loader import (
    DEFAULT_DATA_PATH,
    load_customers,
    validate_customer_record,
)
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
    normalize_text,
    search,
    validate_search_term,
)

__all__ = [
    "DEFAULT_DATA_PATH",
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
    "normalize_text",
    "run_search_cli",
    "search",
    "validate_customer_record",
    "validate_search_term",
]
