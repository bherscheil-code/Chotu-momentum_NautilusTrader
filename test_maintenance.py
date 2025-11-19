#!/usr/bin/env python3
"""
test_maintenance.py
Quick test to verify maintenance script prerequisites
"""

import sys
import subprocess
import shutil
from pathlib import Path


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (need 3.8+)")
        return False


def check_command(cmd):
    """Check if a command is available."""
    if shutil.which(cmd):
        print(f"✅ {cmd} installed")
        return True
    else:
        print(f"⚠️  {cmd} not installed (optional)")
        return False


def check_module(module_name, display_name=None):
    """Check if a Python module can be imported."""
    if display_name is None:
        display_name = module_name
    
    try:
        __import__(module_name)
        print(f"✅ {display_name} installed")
        return True
    except ImportError:
        print(f"❌ {display_name} not installed (required)")
        return False


def check_git_status():
    """Check Git repository status."""
    try:
        result = subprocess.run(
            ["git", "status"],
            capture_output=True,
            text=True,
            check=True
        )
        print("✅ Git repository OK")
        return True
    except subprocess.CalledProcessError:
        print("❌ Not a Git repository or Git not installed")
        return False
    except FileNotFoundError:
        print("❌ Git not installed")
        return False


def main():
    print("=" * 60)
    print("🔍 Maintenance Script Prerequisites Check")
    print("=" * 60)
    print()
    
    all_ok = True
    
    # Check Python version
    print("Python Environment:")
    print("-" * 60)
    if not check_python_version():
        all_ok = False
    print()
    
    # Check required commands
    print("Required Commands:")
    print("-" * 60)
    if not check_command("git"):
        all_ok = False
    check_command("pip")
    print()
    
    # Check optional commands
    print("Optional Commands (for code optimization):")
    print("-" * 60)
    check_command("black")
    check_command("isort")
    check_command("ruff")
    print()
    
    # Check required Python modules
    print("Required Python Modules:")
    print("-" * 60)
    required_modules = [
        ("nautilus_trader", "nautilus-trader"),
        ("yfinance", "yfinance"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
    ]
    
    for module, display in required_modules:
        if not check_module(module, display):
            all_ok = False
    print()
    
    # Check optional Python modules
    print("Optional Python Modules:")
    print("-" * 60)
    check_module("matplotlib", "matplotlib")
    check_module("seaborn", "seaborn")
    check_module("plotly", "plotly")
    check_module("jupyter", "jupyter")
    print()
    
    # Check Git status
    print("Git Repository:")
    print("-" * 60)
    if not check_git_status():
        all_ok = False
    print()
    
    # Check maintenance scripts exist
    print("Maintenance Scripts:")
    print("-" * 60)
    if Path("maintain-chotu-momentum.bat").exists():
        print("✅ maintain-chotu-momentum.bat found")
    else:
        print("⚠️  maintain-chotu-momentum.bat not found")
    
    if Path("maintain_chotu_momentum.py").exists():
        print("✅ maintain_chotu_momentum.py found")
    else:
        print("⚠️  maintain_chotu_momentum.py not found")
    print()
    
    # Check project files
    print("Project Files:")
    print("-" * 60)
    project_files = [
        "requirements.txt",
        "momentum_walkforward_core.py",
        "nautilus_engine_momentum.py",
    ]
    
    for file in project_files:
        if Path(file).exists():
            print(f"✅ {file} found")
        else:
            print(f"⚠️  {file} not found")
    print()
    
    # Final summary
    print("=" * 60)
    if all_ok:
        print("✅ All required prerequisites met!")
        print("You can run the maintenance script:")
        print()
        print("  Windows:      maintain-chotu-momentum.bat")
        print("  Cross-platform: python maintain_chotu_momentum.py")
    else:
        print("❌ Some required prerequisites are missing.")
        print()
        print("Install missing requirements:")
        print("  pip install -r requirements.txt")
        print()
        print("Install optional tools:")
        print("  pip install black isort ruff")
    print("=" * 60)
    print()
    
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
