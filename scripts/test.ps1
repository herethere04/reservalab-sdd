param(
    [string]$Python = "python",
    [string]$OutputDir = ""
)
$ErrorActionPreference = "Stop"
$testRunner = Join-Path $PSScriptRoot "run_tests.py"
if ($OutputDir) {
    & $Python $testRunner --output-dir $OutputDir
} else {
    & $Python $testRunner
}
exit $LASTEXITCODE
