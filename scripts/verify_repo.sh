#!/usr/bin/env bash
set -euo pipefail

# Determine repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

export PYTHONPATH="src"
export PYTHONDONTWRITEBYTECODE=1

echo "[1/6] Checking repository contract readiness & secret scanning"
python scripts/check_repo_contract.py

echo "[2/6] Verifying protected files integrity & filesystem permissions"
python -c '
import hashlib, os, sys

PROTECTED_FILES = {
    "data/customers.json": "2f50166268e740a8952a0a7fc55e8f6ac81d2904188614a7a5f25f83401abe25",
    "REQUIREMENTS.md": "063e59607df7e905156b3f43277d4edb9c3a82d2b27941eb65b6861ec8c98636",
    "SPEC.md": "273f4e0345917e8414382e7d8cdad0ddf2b6e9c1a9d7fe170ba2dc01b2f42af1",
}

for path, expected in PROTECTED_FILES.items():
    if not os.path.exists(path):
        print(f"ERROR: Protected file {path} is missing!", file=sys.stderr)
        sys.exit(1)
    with open(path, "rb") as f:
        content = f.read()
    norm = hashlib.sha256(content.replace(b"\r\n", b"\n")).hexdigest().lower()
    if norm != expected.lower():
        print(f"ERROR: Protected file {path} has been modified or corrupted!", file=sys.stderr)
        print(f"Expected: {expected}", file=sys.stderr)
        print(f"Actual:   {norm}", file=sys.stderr)
        sys.exit(1)

# Verify filesystem-level read-only protection on data/customers.json
try:
    with open("data/customers.json", "a") as f:
        f.write(" ")
    print("ERROR: data/customers.json is writable; expected filesystem read-only attribute!", file=sys.stderr)
    sys.exit(1)
except PermissionError:
    pass
except Exception as e:
    print(f"ERROR: Unable to verify filesystem permissions: {e}", file=sys.stderr)
    sys.exit(1)
'

echo "[3/6] Checking code formatting (ruff format)"
ruff format --check .

echo "[4/6] Running linter (ruff check)"
ruff check .

echo "[5/6] Running static type checker (mypy)"
mypy src tests

echo "[6/6] Running test suite with coverage & reports (pytest)"
python -m pytest

echo "Checking repository cleanliness"
if command -v git >/dev/null 2>&1; then
    PYC_TRACKED=$(git ls-files "*.pyc" || true)
    if [ -n "${PYC_TRACKED}" ]; then
        echo "ERROR: Compiled bytecode (*.pyc) files are tracked in git index:" >&2
        echo "${PYC_TRACKED}" >&2
        exit 1
    fi
    PYC_FILES=$(git status --porcelain | grep -E '^(\?\?|.[MRA]).*\.pyc$' || true)
    if [ -n "${PYC_FILES}" ]; then
        echo "ERROR: Untracked or modified compiled bytecode (*.pyc) files detected:" >&2
        echo "${PYC_FILES}" >&2
        exit 1
    fi
fi

echo "VERIFY_REPO: PASS"
