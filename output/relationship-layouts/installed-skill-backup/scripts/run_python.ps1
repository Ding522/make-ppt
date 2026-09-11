<#
Run a Python script or command with the first working Python 3.9+ interpreter.

Usage:
  powershell -NoProfile -ExecutionPolicy Bypass -File run_python.ps1 script.py arg1
  powershell -NoProfile -ExecutionPolicy Bypass -File run_python.ps1 -c "import pptx"
#>
param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$PythonArgs
)

$ErrorActionPreference = "Stop"

if (-not $PythonArgs -or $PythonArgs.Count -eq 0) {
  Write-Error "Usage: run_python.ps1 <script.py|-c> [args...]"
  exit 2
}

$candidates = @(
  @{ Name = "py"; Prefix = @("-3") },
  @{ Name = "python"; Prefix = @() },
  @{ Name = "python3"; Prefix = @() }
)

foreach ($candidate in $candidates) {
  $command = Get-Command $candidate.Name -ErrorAction SilentlyContinue
  if (-not $command) {
    continue
  }

  & $command.Source @($candidate.Prefix) -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 9) else 1)" 2>$null
  if ($LASTEXITCODE -ne 0) {
    continue
  }

  & $command.Source @($candidate.Prefix) @PythonArgs
  exit $LASTEXITCODE
}

Write-Error "No working Python 3.9+ interpreter found. Tried py -3, python, and python3."
exit 1
