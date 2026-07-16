@echo off
cd /d "%~dp0"
set /p URL="Paste YouTube URL: "
chcp 65001 >nul
"..\.venv\Scripts\python.exe" summarize.py "%URL%"
echo.
pause
