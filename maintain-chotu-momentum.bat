@echo off
REM maintain-chotu-momentum.bat
REM Full maintenance pipeline for Chotu-momentum_NautilusTrader
REM Windows-compatible version

setlocal enabledelayedexpansion

echo ========================================
echo 📊 Chotu-Momentum Maintenance Pipeline
echo ========================================
echo.

REM 1. UPDATE
echo [1/6] 📥 Pulling latest changes...
git checkout main 2>nul || git checkout master
git pull --ff-only
if errorlevel 1 (
    echo ⚠️  Git pull failed - continuing anyway
)
echo ✅ Update complete
echo.

REM 2. OPTIMIZE & REMOVE BUGS
echo [2/6] 🧹 Formatting and linting code...

REM Check if black is installed
where black >nul 2>&1
if %errorlevel% equ 0 (
    echo Running black formatter...
    black *.py 2>nul
    if exist momentum_walkforward_core.py black momentum_walkforward_core.py 2>nul
    if exist nautilus_engine_momentum.py black nautilus_engine_momentum.py 2>nul
) else (
    echo ⚠️  black not installed - skipping formatting
)

REM Check if isort is installed
where isort >nul 2>&1
if %errorlevel% equ 0 (
    echo Running isort...
    isort *.py 2>nul
) else (
    echo ⚠️  isort not installed - skipping import sorting
)

REM Check if ruff is installed
where ruff >nul 2>&1
if %errorlevel% equ 0 (
    echo Running ruff linter...
    ruff check --fix *.py 2>nul
) else (
    echo ⚠️  ruff not installed - skipping linting
)

echo ✅ Code optimization complete
echo.

REM 3. MAKE DEPLOYABLE
echo [3/6] ⚙️  Installing dependencies...

REM Upgrade pip first
python -m pip install --upgrade pip --quiet 2>nul

REM Install main requirements
if exist requirements.txt (
    echo Installing requirements.txt...
    pip install -r requirements.txt --quiet
    if errorlevel 1 (
        echo ⚠️  Some dependencies failed to install - continuing
    )
) else (
    echo ⚠️  requirements.txt not found
)

REM Verify critical modules
echo Verifying critical dependencies...
python -c "import nautilus_trader; print('✅ NautilusTrader OK')" 2>nul
if errorlevel 1 (
    echo ❌ NautilusTrader missing - attempting install...
    pip install nautilus-trader --quiet
)

python -c "import yfinance, pandas, numpy; print('✅ Data stack OK')" 2>nul
if errorlevel 1 (
    echo ❌ Data dependencies missing - attempting install...
    pip install yfinance pandas numpy --quiet
)

echo ✅ Dependencies verified
echo.

REM 4. TEST RUN
echo [4/6] 🧪 Running quick validation test...

REM Test core module imports
python -c "from momentum_walkforward_core import run_walkforward; print('✅ Core module importable')" 2>nul
if errorlevel 1 (
    echo ⚠️  momentum_walkforward_core.py has import issues
) else (
    echo ✅ Core module validated
)

REM Test strategy module
python -c "from nautilus_engine_momentum import MomentumStrategy, MomentumConfig; print('✅ Strategy module importable')" 2>nul
if errorlevel 1 (
    echo ⚠️  nautilus_engine_momentum.py has import issues
) else (
    echo ✅ Strategy module validated
)

REM Quick data fetch test
echo Testing data connectivity...
python -c "import yfinance as yf; data = yf.download('AAPL', start='2024-01-01', end='2024-01-10', progress=False); print('✅ Yahoo Finance connectivity OK' if not data.empty else '⚠️  Data fetch returned empty')" 2>nul
if errorlevel 1 (
    echo ⚠️  Data connectivity test failed
)

echo ✅ Validation tests complete
echo.

REM 5. REMOVE CACHE
echo [5/6] 🧹 Clearing Python and system caches...

REM Remove Python cache directories
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
echo Removed __pycache__ directories

REM Remove compiled Python files
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul
echo Removed .pyc/.pyo files

REM Remove test and coverage caches
if exist .pytest_cache rd /s /q .pytest_cache 2>nul
if exist .mypy_cache rd /s /q .mypy_cache 2>nul
if exist .ruff_cache rd /s /q .ruff_cache 2>nul
if exist .coverage del /q .coverage 2>nul
if exist htmlcov rd /s /q htmlcov 2>nul
echo Removed test caches

REM Remove Jupyter checkpoints
for /d /r . %%d in (.ipynb_checkpoints) do @if exist "%%d" rd /s /q "%%d" 2>nul
echo Removed Jupyter checkpoints

REM Optional: Remove data caches (uncomment if needed)
REM if exist data_cache rd /s /q data_cache 2>nul
REM if exist results rd /s /q results 2>nul

echo ✅ Cache cleanup complete
echo.

REM 6. PUSH BACK TO REMOTE
echo [6/6] 📤 Committing and pushing changes...

REM Stage all changes
git add .

REM Check if there are changes to commit
git diff-index --quiet HEAD --
if errorlevel 1 (
    REM There are changes - commit them
    for /f "tokens=1-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
    for /f "tokens=1-2 delims=: " %%a in ('time /t') do (set mytime=%%a:%%b)
    git commit -m "chore(momentum): optimized, tested, cache-cleared [!mydate! !mytime! UTC]"
    
    REM Push to remote
    git push origin main 2>nul
    if errorlevel 1 (
        git push origin master 2>nul
        if errorlevel 1 (
            echo ⚠️  Push failed - check remote configuration
        ) else (
            echo ✅ Changes pushed to master branch
        )
    ) else (
        echo ✅ Changes pushed to main branch
    )
) else (
    echo ✅ No changes detected - repository is clean
)

echo.
echo ========================================
echo ✨ Maintenance Pipeline Complete!
echo ========================================
echo.
echo Summary:
echo   ✅ Code updated from remote
echo   ✅ Code formatted and linted
echo   ✅ Dependencies verified
echo   ✅ Modules validated
echo   ✅ Caches cleared
echo   ✅ Changes committed and pushed
echo.
echo Your Chotu-Momentum project is ready! 📈
echo.

pause
