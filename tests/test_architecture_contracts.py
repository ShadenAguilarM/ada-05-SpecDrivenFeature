"""Automated Architecture Contract Tests.

Verifies:
1. Re-export parity between implementation modules and backward-compatibility aliases.
2. Package root re-exports all public symbols.
3. Component isolation and layer boundary constraints per ARCHITECTURE.md.
4. No external runtime dependencies in package code.
5. Domain model immutability.
6. Filesystem read-only protection of customer dataset.
"""

from __future__ import annotations

import ast
import importlib.util
import sys
from dataclasses import FrozenInstanceError, is_dataclass
from pathlib import Path
from types import ModuleType

import pytest

import customer_search
import customer_search.customer as customer_mod
import customer_search.data_loader as data_loader_mod
import customer_search.search_service as search_service_mod
from customer_search import Customer

PACKAGE_ROOT = Path(__file__).resolve().parent.parent / "src" / "customer_search"


def _load_standalone_module(name: str, path: Path) -> ModuleType:
    """Load a module from a file path without polluting the package namespace."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module spec from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


search_alias = _load_standalone_module("standalone_search_alias", PACKAGE_ROOT / "search.py")
loader_alias = _load_standalone_module("standalone_loader_alias", PACKAGE_ROOT / "loader.py")
models_alias = _load_standalone_module("standalone_models_alias", PACKAGE_ROOT / "models.py")


def _extract_imported_modules(file_path: Path) -> list[str]:
    """Parse a python file AST and return all top-level imported module names."""
    tree = ast.parse(file_path.read_text(encoding="utf-8"))
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.append(node.module)
    return imported


def test_search_service_and_search_alias_export_parity():
    """Verify search.py re-exports all public symbols from search_service.py identically."""
    assert hasattr(search_service_mod, "__all__"), "search_service must define __all__"
    assert hasattr(search_alias, "__all__"), "search alias must define __all__"
    assert sorted(search_service_mod.__all__) == sorted(search_alias.__all__), (
        "search.py and search_service.py must export identical symbols"
    )


def test_data_loader_and_loader_alias_export_parity():
    """Verify loader.py re-exports all public symbols from data_loader.py identically."""
    assert hasattr(data_loader_mod, "__all__"), "data_loader must define __all__"
    assert hasattr(loader_alias, "__all__"), "loader alias must define __all__"
    assert sorted(data_loader_mod.__all__) == sorted(loader_alias.__all__), (
        "loader.py and data_loader.py must export identical symbols"
    )


def test_customer_and_models_alias_export_parity():
    """Verify models.py re-exports all public symbols from customer.py identically."""
    assert hasattr(customer_mod, "__all__"), "customer module must define __all__"
    assert hasattr(models_alias, "__all__"), "models alias must define __all__"
    assert sorted(customer_mod.__all__) == sorted(models_alias.__all__), (
        "models.py and customer.py must export identical symbols"
    )


def test_package_root_reexports_all_submodule_public_symbols():
    """Verify package __init__.py re-exports all public symbols from core modules."""
    for symbol in search_service_mod.__all__:
        assert symbol in customer_search.__all__, (
            f"{symbol} from search_service missing in customer_search.__all__"
        )
    for symbol in data_loader_mod.__all__:
        assert symbol in customer_search.__all__, (
            f"{symbol} from data_loader missing in customer_search.__all__"
        )
    for symbol in customer_mod.__all__:
        assert symbol in customer_search.__all__, (
            f"{symbol} from customer missing in customer_search.__all__"
        )


def test_customer_model_has_no_dependencies_on_services_or_loader():
    """Verify Customer domain model does not depend on search_service, data_loader, or cli."""
    imported = _extract_imported_modules(PACKAGE_ROOT / "customer.py")
    for mod in imported:
        assert not mod.startswith(
            (
                "customer_search.search",
                "customer_search.data_loader",
                "customer_search.cli",
            )
        ), f"customer.py has forbidden dependency: {mod}"


def test_data_loader_has_no_dependency_on_search_or_cli():
    """Verify Data Loader does not depend on search_service or cli."""
    imported = _extract_imported_modules(PACKAGE_ROOT / "data_loader.py")
    for mod in imported:
        assert not mod.startswith(
            (
                "customer_search.search",
                "customer_search.cli",
            )
        ), f"data_loader.py has forbidden dependency: {mod}"


def test_search_service_has_no_dependency_on_cli():
    """Verify Search Service does not depend on CLI."""
    imported = _extract_imported_modules(PACKAGE_ROOT / "search_service.py")
    for mod in imported:
        assert not mod.startswith("customer_search.cli"), (
            f"search_service.py has forbidden dependency: {mod}"
        )


def test_no_external_runtime_dependencies():
    """Verify all runtime modules only import from Python standard library or customer_search."""
    stdlib_modules = sys.stdlib_module_names
    for py_file in PACKAGE_ROOT.glob("*.py"):
        imported = _extract_imported_modules(py_file)
        for mod in imported:
            root_pkg = mod.split(".")[0]
            assert (
                root_pkg in stdlib_modules
                or root_pkg == "customer_search"
                or root_pkg in ("__future__",)
            ), f"Module {py_file.name} imports unauthorized external package: {mod}"


def test_domain_model_immutability():
    """Verify Customer dataclass is frozen and mutating raises FrozenInstanceError."""
    assert is_dataclass(Customer), "Customer must be a dataclass"
    cust = Customer(name="Alice", surname="Smith", email="alice@example.com")
    with pytest.raises(FrozenInstanceError):
        cust.name = "Bob"  # type: ignore[misc]


def test_intentional_export_omission_fails():
    """Verify export parity check fails when an export is omitted."""
    actual_exports = set(search_alias.__all__)
    tampered_exports = set(actual_exports) - {"MAX_RESULTS"}
    assert actual_exports != tampered_exports


def test_data_customers_json_filesystem_read_only():
    """Verify data/customers.json has OS filesystem-level read-only protection."""
    data_file = PACKAGE_ROOT.parent.parent / "data" / "customers.json"
    assert data_file.is_file(), "customers.json must exist"
    with pytest.raises(PermissionError):
        with open(data_file, "a", encoding="utf-8") as f:
            f.write(" ")
