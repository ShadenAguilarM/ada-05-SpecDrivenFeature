$ErrorActionPreference = "Stop"

# Determine repository root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
Set-Location $RepoRoot

$env:PYTHONPATH = "src"
$env:PYTHONDONTWRITEBYTECODE = "1"

Write-Host "[1/4] Checking repository contract readiness..."
python scripts/check_repo_contract.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "Repository contract check failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

Write-Host "[2/4] Verifying protected files integrity..."
python -c @"
import hashlib, os, sys

PROTECTED_FILES = {
    'data/customers.json': '2f50166268e740a8952a0a7fc55e8f6ac81d2904188614a7a5f25f83401abe25',
    'REQUIREMENTS.md': '063e59607df7e905156b3f43277d4edb9c3a82d2b27941eb65b6861ec8c98636',
    'SPEC.md': '273f4e0345917e8414382e7d8cdad0ddf2b6e9c1a9d7fe170ba2dc01b2f42af1',
}

for path, expected in PROTECTED_FILES.items():
    if not os.path.exists(path):
        print(f'ERROR: Protected file {path} is missing!', file=sys.stderr)
        sys.exit(1)
    with open(path, 'rb') as f:
        content = f.read()
    norm = hashlib.sha256(content.replace(b'\r\n', b'\n')).hexdigest().lower()
    if norm != expected.lower():
        print(f'ERROR: Protected file {path} has been modified or corrupted!', file=sys.stderr)
        print(f'Expected: {expected}', file=sys.stderr)
        print(f'Actual:   {norm}', file=sys.stderr)
        sys.exit(1)
"@
if ($LASTEXITCODE -ne 0) {
    Write-Error "Protected files integrity verification failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

Write-Host "[3/4] Running tests (pytest)..."
python -m pytest -v
if ($LASTEXITCODE -ne 0) {
    Write-Error "Test suite failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

Write-Host "[4/4] Checking repository cleanliness..."
$gitCmd = Get-Command git -ErrorAction SilentlyContinue
if ($gitCmd) {
    $pycFiles = git status --porcelain | Select-String '\.pyc$'
    if ($pycFiles) {
        Write-Error "Untracked or modified compiled bytecode (*.pyc) files detected:`n$pycFiles"
        exit 1
    }
}

Write-Host "VERIFY_REPO: PASS"
exit 0
