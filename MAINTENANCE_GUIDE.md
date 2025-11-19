# Chotu-Momentum Maintenance Guide

This guide explains how to use the automated maintenance scripts for the Chotu-momentum_NautilusTrader project.

## 📋 What the Maintenance Scripts Do

The maintenance pipeline performs 6 key steps:

1. **Update** - Pulls latest changes from Git
2. **Optimize** - Formats and lints code (black, isort, ruff)
3. **Make Deployable** - Installs/updates dependencies
4. **Test Run** - Validates core modules and data connectivity
5. **Remove Cache** - Clears Python caches and temporary files
6. **Push** - Commits changes and pushes to remote

## 🚀 Quick Start

### Option 1: Windows Batch Script (Recommended for Windows)

```cmd
maintain-chotu-momentum.bat
```

**Pros:**
- Native Windows execution
- No Python required to run the script itself
- Simple double-click execution

**Cons:**
- Windows-only
- Less robust error handling

### Option 2: Python Script (Cross-Platform)

```bash
# Windows
python maintain_chotu_momentum.py

# Linux/macOS
python3 maintain_chotu_momentum.py
```

**Pros:**
- Works on Windows, Linux, macOS
- Better error handling
- More detailed output

**Cons:**
- Requires Python to be installed

## 📦 Prerequisites

### Required (for the project itself)
- Python 3.8+
- Git
- pip

### Optional (for code optimization)
- black (code formatter)
- isort (import sorter)
- ruff (linter)

Install optional tools:
```bash
pip install black isort ruff
```

## 🔧 Installation

1. **Clone the repository** (if not already done):
```bash
git clone https://github.com/CRAJKUMARSINGH/Chotu-momentum_NautilusTrader.git
cd Chotu-momentum_NautilusTrader
```

2. **Make scripts executable** (Linux/macOS only):
```bash
chmod +x maintain_chotu_momentum.py
```

3. **Run the maintenance script**:
```bash
# Windows
maintain-chotu-momentum.bat

# Or use Python version
python maintain_chotu_momentum.py
```

## 📝 What Gets Modified

### Files Changed
- `*.py` - Formatted and linted
- `requirements.txt` - Dependencies installed
- Git repository - Changes committed and pushed

### Files/Folders Removed
- `__pycache__/` - Python cache directories
- `*.pyc`, `*.pyo` - Compiled Python files
- `.pytest_cache/` - Pytest cache
- `.mypy_cache/` - MyPy cache
- `.ruff_cache/` - Ruff cache
- `.ipynb_checkpoints/` - Jupyter checkpoints
- `.coverage`, `htmlcov/` - Coverage reports

### Files NOT Modified
- Jupyter notebooks (`*.ipynb`)
- Data files
- Configuration files
- Documentation

## ⚙️ Customization

### Skip Git Operations

Edit the script and comment out the git commands:

**In .bat file:**
```batch
REM git pull --ff-only
REM git push origin main
```

**In .py file:**
```python
# run_command("git pull --ff-only")
# run_command("git push origin main")
```

### Skip Code Formatting

Remove or comment out the black/isort/ruff sections.

### Add Custom Tests

In the "TEST RUN" section, add your own validation:

```python
# Custom test example
print("Running custom validation...")
success, result = run_command(
    f'{sys.executable} -c "import my_module; my_module.test()"',
    capture_output=True
)
```

## 🐛 Troubleshooting

### "Git pull failed"
- **Cause**: Uncommitted local changes or merge conflicts
- **Solution**: Manually resolve conflicts or stash changes
```bash
git stash
git pull
git stash pop
```

### "black/isort/ruff not installed"
- **Cause**: Optional tools not installed
- **Solution**: Install them or ignore the warnings
```bash
pip install black isort ruff
```

### "NautilusTrader missing"
- **Cause**: Core dependency not installed
- **Solution**: The script will attempt auto-install, or manually:
```bash
pip install nautilus-trader
```

### "Push failed"
- **Cause**: No write access to remote or network issues
- **Solution**: Check Git credentials and network
```bash
git remote -v
git config --list
```

### "Data connectivity test failed"
- **Cause**: Network issues or Yahoo Finance API problems
- **Solution**: Check internet connection, try again later

## 🔒 Safety Features

### What's Safe
- ✅ All operations are reversible via Git
- ✅ No data files are deleted
- ✅ Only cache and temporary files are removed
- ✅ Dependencies are installed, not removed

### What to Watch
- ⚠️ Uncommitted changes will be committed automatically
- ⚠️ Code formatting may change style (but not logic)
- ⚠️ Git push requires write access to remote

### Best Practices
1. **Review changes** before running in production
2. **Test on a branch** first
3. **Backup important work** before running
4. **Run during off-hours** to avoid conflicts

## 📅 Recommended Schedule

### Daily (Automated)
- Run maintenance script via cron/Task Scheduler
- Keeps code clean and dependencies updated

### Weekly (Manual)
- Review commit history
- Check for dependency updates
- Run full backtests

### Monthly (Manual)
- Review and optimize parameters
- Update documentation
- Archive old results

## 🤖 Automation Setup

### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., daily at 2 AM)
4. Action: Start a program
5. Program: `C:\path\to\maintain-chotu-momentum.bat`

### Linux/macOS Cron

Add to crontab:
```bash
# Run daily at 2 AM
0 2 * * * cd /path/to/Chotu-momentum_NautilusTrader && python3 maintain_chotu_momentum.py >> maintenance.log 2>&1
```

### CI/CD Integration

Add to GitHub Actions (`.github/workflows/maintenance.yml`):
```yaml
name: Daily Maintenance
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
  workflow_dispatch:  # Manual trigger

jobs:
  maintain:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Run maintenance
        run: python maintain_chotu_momentum.py
```

## 📊 Expected Output

```
============================================================
📊 Chotu-Momentum Maintenance Pipeline
============================================================

[1/6] 📥 Pulling latest changes...
--------------------------------------------------
✅ Update complete

[2/6] 🧹 Formatting and linting code...
--------------------------------------------------
Running black formatter...
Running isort...
Running ruff linter...
✅ Code optimization complete

[3/6] ⚙️  Installing dependencies...
--------------------------------------------------
Upgrading pip...
Installing requirements.txt...
Verifying critical dependencies...
✅ NautilusTrader OK
✅ Data stack OK
✅ Dependencies verified

[4/6] 🧪 Running quick validation test...
--------------------------------------------------
✅ Core module importable
✅ Strategy module importable
Testing data connectivity...
✅ Yahoo Finance connectivity OK
✅ Validation tests complete

[5/6] 🧹 Clearing Python and system caches...
--------------------------------------------------
Removed __pycache__ directories
Removed .pyc/.pyo files
Removed test caches
Removed Jupyter checkpoints
✅ Cache cleanup complete

[6/6] 📤 Committing and pushing changes...
--------------------------------------------------
✅ Changes pushed to main branch

============================================================
✨ Maintenance Pipeline Complete!
============================================================

Summary:
  ✅ Code updated from remote
  ✅ Code formatted and linted
  ✅ Dependencies verified
  ✅ Modules validated
  ✅ Caches cleared
  ✅ Changes committed and pushed

Your Chotu-Momentum project is ready! 📈
```

## 🆘 Support

For issues specific to:
- **Maintenance scripts**: Check this guide
- **NautilusTrader**: See [NautilusTrader docs](https://nautilustrader.io/)
- **Strategy logic**: See `README.md` and `WHAT_IS_IN_THE_APP.md`
- **Project setup**: See main `README.md`

## 📄 License

Same as the main project (see LICENSE file).
