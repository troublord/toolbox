@echo off
cd /d "%~dp0"
set /p URL="Paste YouTube URL: "
"..\.venv\Scripts\python.exe" summarize.py "%URL%"
echo.
pause
