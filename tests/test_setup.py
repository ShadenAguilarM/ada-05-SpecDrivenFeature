"""Verification tests for project setup (T-01)."""

import sys


def test_python_version():
    """Verify that Python version is 3.11 or higher (C-01)."""
    assert sys.version_info >= (3, 11), f"Python 3.11+ required, got {sys.version}"
