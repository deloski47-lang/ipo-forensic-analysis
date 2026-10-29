$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Backend = Join-Path $Root "backend"
$Frontend = Join-Path $Root "frontend"
$Venv = Join-Path $Backend ".venv"
$Python = if (Get-Command py -ErrorAction SilentlyContinue) { "py" } else { "python" }

if (-not (Get-Command node -ErrorAction SilentlyContinue)) { throw "Node.js 22+ is required. Install Node.js, then rerun this script." }
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) { throw "npm is required with Node.js." }
if (-not (Test-Path $Venv)) { & $Python -3 -m venv $Venv; if ($LASTEXITCODE -ne 0) { & $Python -m venv $Venv } }
$PyExe = Join-Path $Venv "Scripts\python.exe"
$PipExe = Join-Path $Venv "Scripts\pip.exe"
& $PipExe install -e "[$((Get-Location).Path)]" 2>$null
if ($LASTEXITCODE -ne 0) { & $PipExe install -e $Backend }
if ($LASTEXITCODE -ne 0) { throw "Backend dependencies could not be installed." }
Push-Location $Frontend
try {
  if (-not (Test-Path "node_modules")) { npm install }
  if ($LASTEXITCODE -ne 0) { throw "Frontend dependencies could not be installed." }
} finally { Pop-Location }
$BackendProcess = Start-Process -FilePath $PyExe -ArgumentList @("-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000") -WorkingDirectory $Backend -PassThru
Start-Sleep -Seconds 2
$FrontendProcess = Start-Process -FilePath "npm" -ArgumentList @("run", "dev") -WorkingDirectory $Frontend -PassThru
Write-Host ""
Write-Host "IPO Forensic Analysis Engine is starting."
Write-Host "Frontend: http://127.0.0.1:5173"
Write-Host "API docs:  http://127.0.0.1:8000/docs"
Write-Host "Close this window to stop tracking the launch. Stop the spawned processes from Task Manager when finished."
Write-Host "Backend PID: $($BackendProcess.Id) | Frontend PID: $($FrontendProcess.Id)"
