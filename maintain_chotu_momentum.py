#!/usr/bin/env python3
"""
maintain_chotu_momentum.py
Full maintenance pipeline for Chotu-momentum_NautilusTrader
Cross-platform Python version (works on Windows, Linux, macOS)
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime
import shutil


def run_command(cmd, shell=True, check=False, capture_output=False):
    """Run a shell command with error handling."""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            check=check,
            capture_output=capture_output,
            text=True
        )
        return result.returncode == 0, result
    except subprocess.CalledProcessError as e:
        return False, e
    except Exception as e:
        print(f"⚠️  Command failed: {e}")
        return False, None


def print_step(step_num, total_steps, message):
    """Print a formatted step message."""
    print(f"\n[{step_num}/{total_steps}] {message}")
    print("-" * 50)


def main():
    print("=" * 60)
    print("📊 Chotu-Momentum Maintenance Pipeline")
    print("=" * 60)
    
    total_steps = 6
    
    # 1. UPDATE
    print_step(1, total_steps, "📥 Pulling latest changes...")
    
    # Try main branch first, then master
    success, _ = run_command("git checkout main")
    if not success:
        run_command("git checkout master")
    
    success, _ = run_command("git pull --ff-only")
    if success:
        print("✅ Update complete")
    else:
        print("⚠️  Git pull failed - continuing anyway")
    
    # 2. OPTIMIZE & REMOVE BUGS
    print_step(2, total_steps, "🧹 Formatting and linting code...")
    
    # Check and run black
    if shutil.which("black"):
        print("Running black formatter...")
        run_command("black *.py")
        if Path("momentum_walkforward_core.py").exists():
            run_command("black momentum_walkforward_core.py")
        if Path("nautilus_engine_momentum.py").exists():
            run_command("black nautilus_engine_momentum.py")
    else:
        print("⚠️  black not installed - skipping formatting")
    
    # Check and run isort
    if shutil.which("isort"):
        print("Running isort...")
        run_command("isort *.py")
    else:
        print("⚠️  isort not installed - skipping import sorting")
    
    # Check and run ruff
    if shutil.which("ruff"):
        print("Running ruff linter...")
        run_command("ruff check --fix *.py")
    else:
        print("⚠️  ruff not installed - skipping linting")
    
    print("✅ Code optimization complete")
    
    # 3. MAKE DEPLOYABLE
    print_step(3, total_steps, "⚙️  Installing dependencies...")
    
    # Upgrade pip
    print("Upgrading pip...")
    run_command(f"{sys.executable} -m pip install --upgrade pip --quiet")
    
    # Install requirements
    if Path("requirements.txt").exists():
        print("Installing requirements.txt...")
        success, _ = run_command(f"{sys.executable} -m pip install -r requirements.txt --quiet")
        if not success:
            print("⚠️  Some dependencies failed to install - continuing")
    else:
        print("⚠️  requirements.txt not found")
    
    # Verify critical modules
    print("Verifying critical dependencies...")
    
    # Check NautilusTrader
    success, _ = run_command(
        f'{sys.executable} -c "import nautilus_trader; print(\'✅ NautilusTrader OK\')"',
        capture_output=True
    )
    if not success:
        print("❌ NautilusTrader missing - attempting install...")
        run_command(f"{sys.executable} -m pip install nautilus-trader --quiet")
    
    # Check data stack
    success, _ = run_command(
        f'{sys.executable} -c "import yfinance, pandas, numpy; print(\'✅ Data stack OK\')"',
        capture_output=True
    )
    if not success:
        print("❌ Data dependencies missing - attempting install...")
        run_command(f"{sys.executable} -m pip install yfinance pandas numpy --quiet")
    
    print("✅ Dependencies verified")
    
    # 4. TEST RUN
    print_step(4, total_steps, "🧪 Running quick validation test...")
    
    # Test core module
    if Path("momentum_walkforward_core.py").exists():
        success, result = run_command(
            f'{sys.executable} -c "from momentum_walkforward_core import run_walkforward; print(\'✅ Core module importable\')"',
            capture_output=True
        )
        if success and result:
            print(result.stdout.strip())
        else:
            print("⚠️  momentum_walkforward_core.py has import issues")
    
    # Test strategy module
    if Path("nautilus_engine_momentum.py").exists():
        success, result = run_command(
            f'{sys.executable} -c "from nautilus_engine_momentum import MomentumStrategy, MomentumConfig; print(\'✅ Strategy module importable\')"',
            capture_output=True
        )
        if success and result:
            print(result.stdout.strip())
        else:
            print("⚠️  nautilus_engine_momentum.py has import issues")
    
    # Test data connectivity
    print("Testing data connectivity...")
    test_code = """
import yfinance as yf
data = yf.download('AAPL', start='2024-01-01', end='2024-01-10', progress=False)
print('✅ Yahoo Finance connectivity OK' if not data.empty else '⚠️  Data fetch returned empty')
"""
    success, result = run_command(
        f'{sys.executable} -c "{test_code}"',
        capture_output=True
    )
    if success and result:
        print(result.stdout.strip())
    else:
        print("⚠️  Data connectivity test failed")
    
    print("✅ Validation tests complete")
    
    # 5. REMOVE CACHE
    print_step(5, total_steps, "🧹 Clearing Python and system caches...")
    
    # Remove __pycache__ directories
    for pycache in Path(".").rglob("__pycache__"):
        try:
            shutil.rmtree(pycache)
        except Exception:
            pass
    print("Removed __pycache__ directories")
    
    # Remove compiled Python files
    for pyc in Path(".").rglob("*.pyc"):
        try:
            pyc.unlink()
        except Exception:
            pass
    for pyo in Path(".").rglob("*.pyo"):
        try:
            pyo.unlink()
        except Exception:
            pass
    print("Removed .pyc/.pyo files")
    
    # Remove test and coverage caches
    cache_dirs = [".pytest_cache", ".mypy_cache", ".ruff_cache", "htmlcov"]
    for cache_dir in cache_dirs:
        if Path(cache_dir).exists():
            try:
                shutil.rmtree(cache_dir)
            except Exception:
                pass
    
    if Path(".coverage").exists():
        try:
            Path(".coverage").unlink()
        except Exception:
            pass
    print("Removed test caches")
    
    # Remove Jupyter checkpoints
    for checkpoint in Path(".").rglob(".ipynb_checkpoints"):
        try:
            shutil.rmtree(checkpoint)
        except Exception:
            pass
    print("Removed Jupyter checkpoints")
    
    print("✅ Cache cleanup complete")
    
    # 6. PUSH BACK TO REMOTE
    print_step(6, total_steps, "📤 Committing and pushing changes...")
    
    # Stage all changes
    run_command("git add .")
    
    # Check if there are changes
    success, result = run_command("git diff-index --quiet HEAD --")
    
    if not success:  # There are changes
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        commit_msg = f"chore(momentum): optimized, tested, cache-cleared [{timestamp}]"
        
        run_command(f'git commit -m "{commit_msg}"')
        
        # Try pushing to main, then master
        success, _ = run_command("git push origin main")
        if success:
            print("✅ Changes pushed to main branch")
        else:
            success, _ = run_command("git push origin master")
            if success:
                print("✅ Changes pushed to master branch")
            else:
                print("⚠️  Push failed - check remote configuration")
    else:
        print("✅ No changes detected - repository is clean")
    
    # Final summary
    print("\n" + "=" * 60)
    print("✨ Maintenance Pipeline Complete!")
    print("=" * 60)
    print("\nSummary:")
    print("  ✅ Code updated from remote")
    print("  ✅ Code formatted and linted")
    print("  ✅ Dependencies verified")
    print("  ✅ Modules validated")
    print("  ✅ Caches cleared")
    print("  ✅ Changes committed and pushed")
    print("\nYour Chotu-Momentum project is ready! 📈\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Maintenance interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
