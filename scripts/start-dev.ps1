$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Backend = Join-Path $Root "backend"
$Frontend = Join-Path $Root "frontend"
$Venv = Join-Path $Backend ".venv"

if (-not (Get-Command node -ErrorAction SilentlyContinue)) { throw "Node.js 22.22+ is required. Install Node.js, then rerun this script." }
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) { throw "npm is required with Node.js." }

# Use the same supported Python version as CI. Do not let the py launcher silently
# select a bleeding-edge interpreter (for example Python 3.15) with missing wheels.
$PythonLauncher = $null
$PythonPrefixArgs = @()
if (Get-Command py -ErrorAction SilentlyContinue) {
  & py -3.12 --version *> $null
  if ($LASTEXITCODE -eq 0) {
    $PythonLauncher = "py"
    $PythonPrefixArgs = @("-3.12")
  }
}
if (-not $PythonLauncher -and (Get-Command python -ErrorAction SilentlyContinue)) {
  $PythonVersion = (& python --version 2>&1 | Out-String).Trim()
  if ($PythonVersion -match "^Python 3\.12\.") {
    $PythonLauncher = "python"
  }
}
if (-not $PythonLauncher) {
  throw "Python 3.12 is required for a reliable Windows install. Install Python 3.12 from https://www.python.org/downloads/windows/ (enable the Python launcher), then rerun .\scripts\start-dev.ps1. Do not install Visual C++ Build Tools to work around Python 3.15 package builds."
}

$PyExe = Join-Path $Venv "Scripts\python.exe"
$VenvIsSupported = $false
if (Test-Path $PyExe) {
  $VenvVersion = (& $PyExe --version 2>&1 | Out-String).Trim()
  $VenvIsSupported = $VenvVersion -match "^Python 3\.12\."
}
if (-not $VenvIsSupported) {
  if (Test-Path $Venv) { Remove-Item -Recurse -Force $Venv }
  & $PythonLauncher @PythonPrefixArgs -m venv $Venv
  if ($LASTEXITCODE -ne 0) { throw "Could not create the Python 3.12 virtual environment." }
}
$PyExe = Join-Path $Venv "Scripts\python.exe"
& $PyExe -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "Could not upgrade pip in the backend virtual environment." }
& $PyExe -m pip install -e "${Backend}[dev]"
if ($LASTEXITCODE -ne 0) { throw "Backend dependency installation failed. Check the Python version and the pip error above." }

Push-Location $Frontend
try {
  if (-not (Test-Path "node_modules")) { npm install }
  if ($LASTEXITCODE -ne 0) { throw "Frontend dependencies could not be installed." }
} finally { Pop-Location }

$BackendProcess = Start-Process -FilePath $PyExe -ArgumentList @("-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000") -WorkingDirectory $Backend -PassThru
Start-Sleep -Seconds 2
$FrontendProcess = Start-Process -FilePath "cmd.exe" -ArgumentList @("/c", "npm run dev") -WorkingDirectory $Frontend -PassThru
Write-Host ""
Write-Host "IPO Forensic Analysis Engine is starting."
Write-Host "Frontend: http://127.0.0.1:5173"
Write-Host "API docs:  http://127.0.0.1:8000/docs"
Write-Host "Close this window to stop tracking the launch. Stop the spawned processes from Task Manager when finished."
Write-Host "Backend PID: $($BackendProcess.Id) | Frontend PID: $($FrontendProcess.Id)"
