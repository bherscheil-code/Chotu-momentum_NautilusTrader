# Quick Maintenance Reference

## 🚀 One-Command Execution

### Windows
```cmd
maintain-chotu-momentum.bat
```

### Cross-Platform
```bash
python maintain_chotu_momentum.py
```

## 📋 What It Does (6 Steps)

| Step | Action | Time |
|------|--------|------|
| 1️⃣ Update | `git pull` | 5s |
| 2️⃣ Optimize | Format & lint code | 10s |
| 3️⃣ Deploy | Install dependencies | 30s |
| 4️⃣ Test | Validate modules | 15s |
| 5️⃣ Clean | Remove caches | 5s |
| 6️⃣ Push | `git commit & push` | 10s |

**Total Time:** ~75 seconds

## ✅ Prerequisites

```bash
# Required
pip install nautilus-trader yfinance pandas numpy

# Optional (for optimization)
pip install black isort ruff
```

## 🔧 Quick Fixes

### Script won't run?
```bash
# Windows
python maintain_chotu_momentum.py

# Linux/macOS - make executable
chmod +x maintain_chotu_momentum.py
./maintain_chotu_momentum.py
```

### Git conflicts?
```bash
git stash
python maintain_chotu_momentum.py
git stash pop
```

### Dependencies failing?
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 🤖 Automate It

### Windows (Task Scheduler)
- Program: `C:\path\to\maintain-chotu-momentum.bat`
- Schedule: Daily at 2 AM

### Linux/macOS (Cron)
```bash
0 2 * * * cd /path/to/project && python3 maintain_chotu_momentum.py
```

## 📊 Success Indicators

Look for these in output:
- ✅ Update complete
- ✅ Code optimization complete
- ✅ Dependencies verified
- ✅ Validation tests complete
- ✅ Cache cleanup complete
- ✅ Changes pushed

## ⚠️ Common Warnings (Safe to Ignore)

- `⚠️ black not installed` - Optional formatter
- `⚠️ isort not installed` - Optional import sorter
- `⚠️ ruff not installed` - Optional linter
- `⚠️ No changes detected` - Nothing to commit

## 🆘 Need Help?

See `MAINTENANCE_GUIDE.md` for detailed troubleshooting.
