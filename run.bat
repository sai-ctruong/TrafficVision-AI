@echo off
echo ================================================
echo Smart Traffic Car Counting System
echo ================================================
echo.
echo Starting application...
echo.

python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error: Application failed to start
    echo Please ensure all dependencies are installed:
    echo   pip install -r requirements.txt
    echo.
    pause
)
