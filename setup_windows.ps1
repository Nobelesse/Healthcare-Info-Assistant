# Run from project root in PowerShell. Does not set or expose admin passwords.
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
Write-Host 'Setting up Healthcare Info Assistant (Python 3.11)...' -ForegroundColor Cyan
py -3.11 -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install --upgrade pip
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
if (-not (Test-Path '.env')) { Copy-Item '.env.example' '.env' }
Write-Host 'Setup done. Edit .env to set ADMIN_INITIAL_PASSWORD, then run:' -ForegroundColor Green
Write-Host '  .\.venv\Scripts\python.exe -m scripts.init_admin'
Write-Host '  .\.venv\Scripts\python.exe -m pytest -q'
Write-Host '  .\.venv\Scripts\python.exe -m streamlit run app.py'
