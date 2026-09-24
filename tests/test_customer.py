"""Unit tests for Customer model (T-02)."""

import pytest
from dataclasses import FrozenInstanceError

from customer_search import Customer
from customer_search.customer import Customer as CustomerDirect
from customer_search.models import Customer as CustomerModel


def test_customer_creation():
    """Verify that a customer can be created with the required fields (T-02, FR-01, FR-07)."""
    customer = Customer(name="John", surname="Doe", email="john.doe@example.com")

    assert customer.name == "John"
    assert customer.surname == "Doe"
    assert customer.email == "john.doe@example.com"


def test_customer_full_name_derivation():
    """Verify that the full name is correctly derived from name and surname (T-02, SR-02)."""
    customer = Customer(name="Alice", surname="Smith", email="alice.smith@example.com")

    assert customer.full_name == "Alice Smith"


def test_customer_full_name_format_with_different_values():
    """Verify full name derivation format is name + ' ' + surname (SR-02)."""
    customer = Customer(name="Maria", surname="Garcia Lopez", email="maria@example.com")
    assert customer.full_name == "Maria Garcia Lopez"


def test_customer_imports():
    """Verify Customer is accessible via package root, customer module, and models module."""
    assert Customer is CustomerDirect
    assert Customer is CustomerModel


def test_customer_equality():
    """Verify Customer equality based on field values."""
    c1 = Customer(name="John", surname="Doe", email="john@example.com")
    c2 = Customer(name="John", surname="Doe", email="john@example.com")
    c3 = Customer(name="Jane", surname="Doe", email="jane@example.com")

    assert c1 == c2
    assert c1 != c3


def test_customer_immutability():
    """Verify Customer instance is immutable (frozen dataclass)."""
    customer = Customer(name="John", surname="Doe", email="john@example.com")
    with pytest.raises((FrozenInstanceError, AttributeError)):
        customer.name = "Jane"  # type: ignore[misc]
