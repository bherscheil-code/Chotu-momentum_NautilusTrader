@echo off
echo ========================================
echo Git LFS Migration Script
echo ========================================
echo.

echo Step 1: Installing Git LFS...
git lfs install
if %errorlevel% neq 0 (
    echo ERROR: Git LFS installation failed
    echo Please install Git LFS from: https://git-lfs.github.com/
    pause
    exit /b 1
)

echo.
echo Step 2: Tracking large files...
git lfs track "*.parquet"
git lfs track "*.csv"
git lfs track "*.h5"

echo.
echo Step 3: Adding .gitattributes...
git add .gitattributes

echo.
echo Step 4: Migrating existing files to LFS...
git lfs migrate import --include="*.parquet,*.csv,*.h5" --everything

echo.
echo Step 5: Pushing LFS objects...
git lfs push --all origin main

echo.
echo ========================================
echo Migration Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Verify files: git lfs ls-files
echo 2. Push changes: git push origin main
echo.
pause
