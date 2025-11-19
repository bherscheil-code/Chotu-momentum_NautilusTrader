# WHAT IS IN THE APP - All 9 Chotu Repositories

**Last Updated:** 2025-11-15

---

## 1. Chotu-FinRL
**Type:** Python - Financial Reinforcement Learning Framework  
**Main Tech:** Python, TensorFlow/PyTorch, Streamlit  
**Purpose:** Deep reinforcement learning for automated stock trading

**What's Inside:**
- DRL algorithms: PPO, A2C, DDPG, SAC, TD3
- Multiple data sources: Yahoo Finance, Alpaca, Binance
- Customizable trading environments
- Built-in technical indicators
- Backtesting capabilities
- Streamlit web dashboard

**Entry Point:** `streamlit_app.py`

---

## 2. Chotu-StockSharp
**Type:** C# - Trading Platform  
**Main Tech:** C#, .NET  
**Purpose:** Universal algorithmic trading platform for global markets

**What's Inside:**
- Connections to 100+ exchanges (crypto, stocks, futures, forex)
- Visual strategy designer
- Embedded C# editor
- Real-time market data
- Order execution engine
- Multiple connectors: Binance, MT4, MT5, Interactive Brokers, etc.

**Entry Point:** `.sln` solution files (Visual Studio)

---

## 3. Chotu-backtesting
**Type:** Python - Backtesting Library  
**Main Tech:** Python, Pandas, Plotly, Streamlit  
**Purpose:** Fast backtesting framework for trading strategies

**What's Inside:**
- Simple, well-documented API
- Blazing fast execution
- Built-in optimizer
- Library of composable strategies
- Interactive visualizations
- Streamlit web interface
- Example strategies (SMA crossover, etc.)

**Entry Point:** `streamlit_app.py` or `demo_backtesting.py`

---

## 4. Chotu-lumibot-dev
**Type:** Python - Trading Bot Framework  
**Main Tech:** Python, Alpaca API, Polygon.io  
**Purpose:** Backtesting and live trading library for stocks, options, crypto

**What's Inside:**
- Unified code for backtesting and live trading
- Support for stocks, options, crypto, futures, FOREX
- Multiple broker integrations
- Strategy examples
- Risk management tools
- Paper trading support

**Entry Point:** Example strategies in `examples/` folder

---

## 5. Chotu-momentum_NautilusTrader
**Type:** Python - Advanced Momentum Strategy Suite  
**Main Tech:** Python, NautilusTrader, Jupyter  
**Purpose:** Professional momentum trading with walk-forward optimization

**What's Inside:**
- Multi-index analysis (SP500, NASDAQ100, DAX40, FTSE100, etc.)
- ROC + trend slope momentum strategy
- NautilusTrader backtesting engine
- Walk-forward optimization
- Comprehensive analytics
- Risk metrics and visualizations

**Entry Point:** Jupyter notebooks (`momentum_top1_nasdaq100_nautilus_v3.ipynb`, `momentum_walkforward_runner.ipynb`)

---

## 6. Chotu-offline-suite
**Type:** TypeScript/React - Web Application  
**Main Tech:** Vite, React, TypeScript, Shadcn-ui, Tailwind CSS  
**Purpose:** Offline-capable web application (Lovable project)

**What's Inside:**
- Modern React application
- Shadcn-ui component library
- Tailwind CSS styling
- Vite build system
- TypeScript for type safety
- Responsive design

**Entry Point:** `npm run dev` (development server)

---

## 7. Chotu-qstrader
**Type:** Python - Quantitative Trading Framework  
**Main Tech:** Python, Pandas  
**Purpose:** Schedule-driven backtesting for long-short equities and ETFs

**What's Inside:**
- Modular backtesting framework
- Schedule-based portfolio construction
- Signal generation decoupled from execution
- Performance statistics and tearsheets
- Example strategies (60/40 portfolio, etc.)
- JSON export for metrics

**Entry Point:** Example scripts in `examples/` folder (e.g., `sixty_forty.py`)

---

## 8. Chotu-stock-analysis-engine
**Type:** Python - Stock Analysis Platform  
**Main Tech:** Python, Celery, Redis, Kubernetes  
**Purpose:** Distributed stock analysis with machine learning

**What's Inside:**
- Distributed task processing with Celery
- Redis for caching
- Kubernetes deployment configs
- Docker containerization
- Machine learning algorithms
- Real-time data processing
- API endpoints

**Entry Point:** Docker compose or Kubernetes deployment

---

## 9. Chotu-vectorbt
**Type:** Python - Vectorized Backtesting  
**Main Tech:** Python, NumPy, Pandas, Plotly, Streamlit  
**Purpose:** Fast vectorized backtesting and portfolio analysis

**What's Inside:**
- Blazing fast vectorized operations
- Built-in indicators (SMA, Bollinger Bands, etc.)
- Portfolio optimization
- Walk-forward analysis
- Interactive visualizations
- Streamlit web dashboard
- Support for multiple assets

**Entry Point:** `streamlit_app.py` or example scripts in `examples/`

---

## Summary Table

| Repository | Type | Main Language | Web Interface | Entry Point |
|-----------|------|---------------|---------------|-------------|
| Chotu-FinRL | ML Trading | Python | ✅ Streamlit | streamlit_app.py |
| Chotu-StockSharp | Trading Platform | C# | ❌ Desktop | .sln files |
| Chotu-backtesting | Backtesting | Python | ✅ Streamlit | streamlit_app.py |
| Chotu-lumibot-dev | Trading Bot | Python | ❌ CLI | examples/*.py |
| Chotu-momentum_NautilusTrader | Momentum Strategy | Python | ❌ Jupyter | *.ipynb |
| Chotu-offline-suite | Web App | TypeScript | ✅ React | npm run dev |
| Chotu-qstrader | Quant Trading | Python | ❌ CLI | examples/*.py |
| Chotu-stock-analysis-engine | Analysis Platform | Python | ❌ API | Docker/K8s |
| Chotu-vectorbt | Vectorized Backtest | Python | ✅ Streamlit | streamlit_app.py |

---

## Technology Stack Overview

**Python-based (7 repos):**
- FinRL, backtesting, lumibot-dev, momentum_NautilusTrader, qstrader, stock-analysis-engine, vectorbt

**C#-based (1 repo):**
- StockSharp

**TypeScript/React-based (1 repo):**
- offline-suite

**Web Interfaces (4 repos):**
- FinRL (Streamlit)
- backtesting (Streamlit)
- vectorbt (Streamlit)
- offline-suite (React/Vite)
