@echo off
echo ========================================
echo Stock Learning Hub - Windows Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Checking virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo [2/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/3] Installing dependencies...
pip install -q -r requirements.txt

echo.
echo ========================================
echo Starting Stock Learning Hub...
echo ========================================
echo.
echo Open your browser to: http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py

pause
