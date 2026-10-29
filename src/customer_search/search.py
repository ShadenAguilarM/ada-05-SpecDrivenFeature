"""Customer search alias module."""

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
    "MAX_RESULTS",
    "MSG_EMPTY_SEARCH",
    "MSG_NO_CUSTOMERS_FOUND",
    "CustomerMatch",
    "InvalidSearchTermError",
    "MatchType",
    "SearchResult",
    "SearchService",
    "classify_match",
    "customer_sort_key",
    "execute_search",
    "normalize_text",
    "search",
    "validate_search_term",
]
