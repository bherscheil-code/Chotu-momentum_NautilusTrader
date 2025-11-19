# Git LFS Setup for Chotu-momentum_NautilusTrader

## ⚠️ Important: This repository uses Git LFS

This repository contains large data files (Parquet, CSV) that are tracked using **Git Large File Storage (LFS)**.

## 🔧 First-Time Setup

### 1. Install Git LFS

**Windows:**
```bash
# Download from: https://git-lfs.github.com/
# Or use Chocolatey:
choco install git-lfs
```

**macOS:**
```bash
brew install git-lfs
```

**Linux:**
```bash
sudo apt-get install git-lfs  # Ubuntu/Debian
sudo yum install git-lfs      # CentOS/RHEL
```

### 2. Initialize Git LFS (One-time)

```bash
git lfs install
```

### 3. Clone the Repository

```bash
git clone https://github.com/CRAJKUMARSINGH/Chotu-momentum_NautilusTrader.git
cd Chotu-momentum_NautilusTrader
```

Git LFS will automatically download the large files.

## 📊 Tracked Files

The following file types are tracked by LFS:
- `*.parquet` - Parquet data files
- `*.csv` - CSV data files
- `*.h5` - HDF5 data files

## 🔍 Verify LFS Files

```bash
# List all LFS files
git lfs ls-files

# Check LFS status
git lfs status
```

## 🚀 For Contributors

If you're adding new large files:

```bash
# Files matching tracked patterns are automatically handled
git add nautilus_data-main/bench_data/*.parquet
git commit -m "Add new data files"
git push
```

## 🐛 Troubleshooting

### Issue: "This repository is over its data quota"
**Solution:** Contact repository owner or upgrade GitHub LFS quota

### Issue: "Git LFS is not installed"
**Solution:** Run `git lfs install` after installing Git LFS

### Issue: Files not downloading
**Solution:** 
```bash
git lfs fetch --all
git lfs pull
```

## 📦 Data Files Location

Large data files are stored in:
- `nautilus_data-main/bench_data/multi_stream_data/` - Multi-stream quotes/trades
- `nautilus_data-main/bench_data/` - Benchmark data

## 💡 Alternative: Download Data Separately

If you don't want to use Git LFS, you can download data files separately:

```python
# download_data.py
import requests
from pathlib import Path

def download_sample_data():
    # Add download logic here
    pass
```

## 📚 Learn More

- [Git LFS Documentation](https://git-lfs.github.com/)
- [GitHub LFS Guide](https://docs.github.com/en/repositories/working-with-files/managing-large-files)
