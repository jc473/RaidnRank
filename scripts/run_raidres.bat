@echo off
setlocal
cd /d "%~dp0"
python raidres.py
if errorlevel 1 (
  echo.
  echo Script failed. See errors above.
)
pause
