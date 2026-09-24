"""Unit tests for JSON Customer Data Loader (T-03)."""

import hashlib
import json
import time
from pathlib import Path

import pytest

from customer_search import Customer, load_customers
from customer_search.data_loader import DEFAULT_DATA_PATH, validate_customer_record
from customer_search.loader import load_customers as load_customers_alias


def test_load_default_customers():
    """Verify loading customers from default JSON data file (A-01, C-02)."""
    assert DEFAULT_DATA_PATH.is_file(), "Default customers.json must exist"
    customers = load_customers()

    assert len(customers) >= 10
    for customer in customers:
        assert isinstance(customer, Customer)
        assert customer.name
        assert customer.surname
        assert customer.email
        assert customer.full_name == f"{customer.name} {customer.surname}"


def test_loader_alias_export():
    """Verify load_customers can be imported from customer_search.loader."""
    assert load_customers is load_customers_alias


def test_load_custom_valid_json_file(tmp_path: Path):
    """Verify loading from a custom valid JSON file."""
    data = [
        {"name": "Ada", "surname": "Lovelace", "email": "ada@example.com"},
        {"name": "Alan", "surname": "Turing", "email": "alan@example.com"},
    ]
    file_path = tmp_path / "custom_customers.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    customers = load_customers(file_path)
    assert len(customers) == 2
    assert customers[0] == Customer(name="Ada", surname="Lovelace", email="ada@example.com")
    assert customers[1] == Customer(name="Alan", surname="Turing", email="alan@example.com")


def test_load_record_with_extra_fields(tmp_path: Path):
    """Verify records with extra fields are accepted and only domain fields are stored."""
    data = [
        {
            "name": "Grace",
            "surname": "Hopper",
            "email": "grace@example.com",
            "age": 85,
            "rank": "Rear Admiral",
        }
    ]
    file_path = tmp_path / "extra_fields.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    customers = load_customers(file_path)
    assert len(customers) == 1
    assert customers[0] == Customer(name="Grace", surname="Hopper", email="grace@example.com")


def test_validate_customer_record():
    """Test individual customer record validation logic (VR-04)."""
    assert validate_customer_record({"name": "A", "surname": "B", "email": "c@d.com"}) is True

    # Non-dictionary
    assert validate_customer_record("invalid") is False
    assert validate_customer_record(123) is False
    assert validate_customer_record(None) is False
    assert validate_customer_record([]) is False

    # Missing fields
    assert validate_customer_record({"surname": "B", "email": "c@d.com"}) is False
    assert validate_customer_record({"name": "A", "email": "c@d.com"}) is False
    assert validate_customer_record({"name": "A", "surname": "B"}) is False

    # Wrong types
    assert validate_customer_record({"name": 123, "surname": "B", "email": "c@d.com"}) is False
    assert validate_customer_record({"name": "A", "surname": None, "email": "c@d.com"}) is False
    assert validate_customer_record({"name": "A", "surname": "B", "email": ["c@d.com"]}) is False

    # Empty or whitespace-only
    assert validate_customer_record({"name": "", "surname": "B", "email": "c@d.com"}) is False
    assert validate_customer_record({"name": "  ", "surname": "B", "email": "c@d.com"}) is False
    assert validate_customer_record({"name": "A", "surname": "  ", "email": "c@d.com"}) is False
    assert validate_customer_record({"name": "A", "surname": "B", "email": ""}) is False


def test_skips_invalid_records_without_unhandled_error(tmp_path: Path):
    """Verify invalid records are filtered out without unhandled error (VR-04, EH-04)."""
    mixed_data = [
        {"name": "Valid", "surname": "One", "email": "one@example.com"},
        {"name": "MissingSurname", "email": "two@example.com"},
        {"name": "MissingEmail", "surname": "Three"},
        {"surname": "MissingName", "email": "four@example.com"},
        {"name": 123, "surname": "WrongType", "email": "five@example.com"},
        {"name": "EmptyName", "surname": "   ", "email": "six@example.com"},
        "not-a-dict",
        12345,
        None,
        [],
        {"name": "Valid", "surname": "Two", "email": "two@example.com"},
    ]
    file_path = tmp_path / "mixed.json"
    file_path.write_text(json.dumps(mixed_data), encoding="utf-8")

    customers = load_customers(file_path)
    assert len(customers) == 2
    assert customers[0].name == "Valid" and customers[0].surname == "One"
    assert customers[1].name == "Valid" and customers[1].surname == "Two"


def test_load_handles_corrupt_json(tmp_path: Path):
    """Verify corrupt JSON file returns empty list without crashing."""
    file_path = tmp_path / "corrupt.json"
    file_path.write_text("{ incomplete json: [", encoding="utf-8")

    customers = load_customers(file_path)
    assert customers == []


def test_load_handles_non_list_root(tmp_path: Path):
    """Verify JSON with non-list root returns empty list without crashing."""
    file_path = tmp_path / "dict_root.json"
    file_path.write_text(json.dumps({"name": "John", "surname": "Doe"}), encoding="utf-8")

    customers = load_customers(file_path)
    assert customers == []


def test_load_handles_missing_file():
    """Verify non-existent file returns empty list without error."""
    missing_path = Path("path/to/definitely/non_existent_file.json")
    customers = load_customers(missing_path)
    assert customers == []


def test_json_data_source_read_only(tmp_path: Path):
    """Verify the JSON data source is strictly read-only and never modified (T-03)."""
    file_path = tmp_path / "readonly_test.json"
    initial_content = json.dumps([{"name": "Test", "surname": "User", "email": "test@example.com"}])
    file_path.write_text(initial_content, encoding="utf-8")

    initial_hash = hashlib.sha256(file_path.read_bytes()).hexdigest()

    # Perform load
    customers = load_customers(file_path)
    assert len(customers) == 1

    post_hash = hashlib.sha256(file_path.read_bytes()).hexdigest()
    assert initial_hash == post_hash, "Data file content must not be modified"
    assert file_path.read_text(encoding="utf-8") == initial_content


def test_load_up_to_10000_customers_performance(tmp_path: Path):
    """Verify loading up to 10,000 customers without error and within 2s (NFR-01, NFR-02)."""
    large_dataset = [
        {
            "name": f"First{i}",
            "surname": f"Last{i}",
            "email": f"user{i}@example.com",
        }
        for i in range(10_000)
    ]
    file_path = tmp_path / "10k_customers.json"
    file_path.write_text(json.dumps(large_dataset), encoding="utf-8")

    start_time = time.perf_counter()
    customers = load_customers(file_path)
    duration = time.perf_counter() - start_time

    assert len(customers) == 10_000
    assert duration < 2.0, f"Loading 10,000 records took {duration:.3f}s, expected < 2s"
