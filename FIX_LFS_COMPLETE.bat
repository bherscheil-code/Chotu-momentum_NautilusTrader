@echo off
echo ========================================
echo Git LFS Migration Script
echo ========================================
echo.

REM Step 1: Install Git LFS
echo [1/7] Installing Git LFS...
git lfs install
if %errorlevel% neq 0 (
    echo ERROR: Git LFS installation failed
    pause
    exit /b 1
)
echo.

REM Step 2: Track parquet files
echo [2/7] Tracking *.parquet files with Git LFS...
git lfs track "*.parquet"
if %errorlevel% neq 0 (
    echo ERROR: Failed to track parquet files
    pause
    exit /b 1
)
echo.

REM Step 3: Add .gitattributes
echo [3/7] Adding .gitattributes...
git add .gitattributes
if %errorlevel% neq 0 (
    echo ERROR: Failed to add .gitattributes
    pause
    exit /b 1
)
echo.

REM Step 4: Remove cached parquet files
echo [4/7] Removing cached parquet files...
git rm -r --cached "nautilus_data-main/bench_data/*.parquet"
if %errorlevel% neq 0 (
    echo WARNING: Some files may not exist in cache, continuing...
)
echo.

REM Step 5: Re-add parquet files
echo [5/7] Re-adding parquet files with LFS...
git add "nautilus_data-main/bench_data/*.parquet"
if %errorlevel% neq 0 (
    echo ERROR: Failed to add parquet files
    pause
    exit /b 1
)
echo.

REM Step 6: Commit changes
echo [6/7] Committing changes...
git commit -m "fix: migrate parquet files to Git LFS"
if %errorlevel% neq 0 (
    echo ERROR: Commit failed
    pause
    exit /b 1
)
echo.

REM Step 7: Push to remote
echo [7/7] Pushing to remote...
echo Pushing LFS objects...
git lfs push --all origin main
if %errorlevel% neq 0 (
    echo ERROR: LFS push failed
    pause
    exit /b 1
)

echo Pushing commits...
git push origin main
if %errorlevel% neq 0 (
    echo ERROR: Git push failed
    pause
    exit /b 1
)
echo.

echo ========================================
echo SUCCESS! LFS migration complete
echo ========================================
pause
