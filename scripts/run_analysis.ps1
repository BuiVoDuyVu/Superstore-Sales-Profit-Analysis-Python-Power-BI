$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $projectRoot ".venv/Scripts/python.exe"
$pythonCommand = if (Test-Path -LiteralPath $venvPython) { $venvPython } else { "python" }

Push-Location -LiteralPath $projectRoot
try {
    & $pythonCommand (Join-Path $projectRoot "src/analyze.py")
    $analysisExitCode = $LASTEXITCODE
}
finally {
    Pop-Location
}
exit $analysisExitCode
