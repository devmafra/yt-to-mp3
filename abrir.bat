@echo off
cd /d "%~dp0"
where pyw >nul 2>&1
if not errorlevel 1 (
  start "" pyw -3 "%~dp0app.py"
  exit /b 0
)
where py >nul 2>&1
if not errorlevel 1 (
  py -3 "%~dp0app.py"
  pause
  exit /b 0
)
where python >nul 2>&1
if not errorlevel 1 (
  python "%~dp0app.py"
  pause
  exit /b 0
)
echo Python nao encontrado. Instale Python 3.10+ para executar o programa.
pause
