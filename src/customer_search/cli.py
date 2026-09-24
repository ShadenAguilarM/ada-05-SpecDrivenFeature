"""Command-line interface for customer search.

Provides interactive and argument-based CLI for searching customer records.
Satisfies: FR-01, FR-05, FR-07, FR-08, NFR-03,
           SR-01, SR-08, SR-09, SR-10, SR-11,
           VR-01, VR-02, VR-03, EH-01, EH-02, EH-03.
"""

from __future__ import annotations

import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

if __package__ is None or __package__ == "":
    src_dir = str(Path(__file__).resolve().parent.parent)
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

from customer_search.customer import Customer
from customer_search.search_service import (
    MSG_EMPTY_SEARCH,
    MSG_NO_CUSTOMERS_FOUND,
    SearchResult,
    SearchService,
    execute_search,
)


def format_customer_display(customer: Customer) -> str:
    """Format a customer record displaying only full name and email address.

    Per FR-07 and SR-08:
    Each search result shall display only:
    - Customer full name.
    - Customer email address.
    """
    return f"{customer.full_name} - {customer.email}"


def format_search_results(result: SearchResult) -> list[str]:
    """Format SearchResult into display lines for the CLI.

    Returns the appropriate message for validation errors or no-results,
    or formatted lines containing each customer's full name and email.
    """
    if result.message:
        return [result.message]

    return [format_customer_display(customer) for customer in result.customers]


def run_search_cli(
    args: Sequence[str] | None = None,
    service: SearchService | None = None,
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
) -> int:
    """Execute the CLI workflow.

    Accepts input either from command-line arguments or prompts interactively.
    Executing when the user presses Enter satisfies SR-10 and NFR-03.

    Args:
        args: Optional list of command-line arguments.
        service: Optional SearchService instance.
        input_func: Function used to read user input (defaults to input).
        output_func: Function used to write output lines (defaults to print).

    Returns:
        Exit code (0 for success, 1 for validation error).
    """
    search_service = service if service is not None else SearchService()

    if args and len(args) > 0:
        query = " ".join(args)
    else:
        try:
            # Prompt user for search term; executes when user presses Enter (NFR-03, SR-10)
            query = input_func("Enter search term: ")
        except (EOFError, KeyboardInterrupt):
            return 0

    result = search_service.execute_search(query)
    lines = format_search_results(result)
    for line in lines:
        output_func(line)

    return 0 if result.is_valid else 1


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point for the customer search CLI application."""
    args = argv if argv is not None else sys.argv[1:]
    return run_search_cli(args=args)


if __name__ == "__main__":
    sys.exit(main())
