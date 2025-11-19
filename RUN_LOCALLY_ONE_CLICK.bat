@echo off
REM ============================================================================
REM ONE-CLICK LOCAL RUN SCRIPT FOR CHOTU-MOMENTUM_NAUTILUSTRADER
REM ============================================================================
REM Last Updated: 2025-11-15
REM ============================================================================

cls
echo ============================================================================
echo           CHOTU-MOMENTUM_NAUTILUSTRADER - MOMENTUM STRATEGY
echo ============================================================================
echo.
echo Starting Chotu-momentum_NautilusTrader (Momentum Strategy Suite)...
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo Please ensure Python is installed and in PATH
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt
pip install jupyter jupyterlab

echo.
echo ============================================================================
echo Starting Jupyter Lab...
echo ============================================================================
echo.
echo Available notebooks:
echo   - momentum_top1_nasdaq100_nautilus_v3.ipynb
echo   - momentum_top1_nasdaq100_nautilus_v5.ipynb
echo   - momentum_walkforward_runner.ipynb
echo.

jupyter lab

pause
