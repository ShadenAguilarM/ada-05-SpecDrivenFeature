"""Customer data loader module.

Loads and validates customer records from a local JSON data source.
Satisfies: A-01, NFR-02, C-02, VR-04, EH-04.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from customer_search.customer import Customer

# Default location for the customer JSON file: <project_root>/data/customers.json
DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "customers.json"


def validate_customer_record(record: Any) -> bool:
    """Validate that a loaded customer record contains the fields required by the domain model.

    Per VR-04 and Domain Model:
    - Must be a dictionary.
    - Must contain non-empty string fields: 'name', 'surname', 'email'.

    Args:
        record: The raw data record to validate.

    Returns:
        True if the record is valid, False otherwise.
    """
    if not isinstance(record, dict):
        return False

    name = record.get("name")
    surname = record.get("surname")
    email = record.get("email")

    if not isinstance(name, str) or not name.strip():
        return False
    if not isinstance(surname, str) or not surname.strip():
        return False
    if not isinstance(email, str) or not email.strip():
        return False

    return True


def load_customers(file_path: str | Path | None = None) -> list[Customer]:
    """Load customer records from a local JSON file.

    Handles invalid customer records and malformed JSON without raising unhandled
    application errors, ensuring read-only access to the data source.

    Args:
        file_path: Optional path to the customer JSON file. Defaults to
            <project_root>/data/customers.json.

    Returns:
        A list of valid Customer domain objects.
    """
    path = Path(file_path) if file_path is not None else DEFAULT_DATA_PATH

    if not path.is_file():
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return []

    if not isinstance(raw_data, list):
        return []

    customers: list[Customer] = []
    for record in raw_data:
        if validate_customer_record(record):
            customers.append(
                Customer(
                    name=record["name"],
                    surname=record["surname"],
                    email=record["email"],
                )
            )

    return customers
