@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if not errorlevel 1 (
  set "PYTHON=py -3"
) else (
  set "PYTHON=python"
)
%PYTHON% -m pip install --upgrade pyinstaller
if errorlevel 1 goto :erro
%PYTHON% -m PyInstaller --noconfirm --clean --onefile --windowed --name ConversorMP3 app.py
if errorlevel 1 goto :erro
echo.
echo Criado: dist\ConversorMP3.exe
pause
exit /b 0
:erro
echo Falha na compilacao. Verifique a instalacao do Python.
pause
exit /b 1
