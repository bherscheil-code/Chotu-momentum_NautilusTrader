"""
Utility functions for Stock Learning Hub
Extracted from parent momentum strategy implementation
"""
import pandas as pd
import numpy as np
import yfinance as yf
from typing import List, Dict, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

def get_stock_data_batch(tickers: List[str], start: str, end: str, min_coverage: float = 0.6) -> pd.DataFrame:
    """
    Download adjusted close prices for multiple tickers
    
    Args:
        tickers: List of stock tickers
        start: Start date (YYYY-MM-DD)
        end: End date (YYYY-MM-DD)
        min_coverage: Minimum data coverage required (0-1)
    
    Returns:
        DataFrame with tickers as columns, dates as index
    """
    try:
        data = yf.download(tickers, start=start, end=end, progress=False, auto_adjust=True, threads=False)
        
        if isinstance(data.columns, pd.MultiIndex) and 'Adj Close' in data.columns.get_level_values(0):
            close = data['Adj Close']
        else:
            close = data['Close'] if isinstance(data.columns, pd.MultiIndex) else data
        
        # Align to business days
        start_ts = pd.to_datetime(start)
        end_ts = pd.to_datetime(end)
        bidx = pd.bdate_range(start=start_ts, end=end_ts, tz=None)
        close = close.reindex(bidx).sort_index()
        
        # Forward fill only
        close = close.ffill()
        
        # Drop symbols with insufficient coverage
        valid_counts = close.notna().sum(axis=0)
        coverage = valid_counts / len(close.index)
        keep = coverage[coverage >= min(min_coverage, 0.5)].index
        close = close[keep]
        
        return close
    except Exception as e:
        print(f"Error downloading data: {e}")
        return pd.DataFrame()

def calculate_momentum_score(prices: pd.Series, lookback: int = 200, roc_period: int = 200) -> Optional[Dict]:
    """
    Calculate momentum score using ROC × Trend Slope methodology
    
    Args:
        prices: Series of prices
        lookback: Days for trend calculation
        roc_period: Days for ROC calculation
    
    Returns:
        Dictionary with momentum metrics or None
    """
    if len(prices) < max(lookback, roc_period):
        return None
    
    try:
        # ROC calculation
        current_price = prices.iloc[-1]
        past_price = prices.iloc[-roc_period]
        
        if past_price <= 0 or np.isnan(past_price) or np.isnan(current_price):
            return None
        
        roc = ((current_price - past_price) / past_price) * 100
        roc_normalized = max(0, min(1, float(np.ceil(roc))))
        
        # Trend slope calculation
        recent_prices = prices.tail(lookback)
        log_prices = np.log(recent_prices.replace(0, np.nan).dropna())
        
        if len(log_prices) < 20:
            return None
        
        x = np.arange(len(log_prices))
        slope = np.polyfit(x, log_prices, 1)[0]
        
        # Momentum score
        score = roc_normalized * slope
        
        if not np.isfinite(score):
            return None
        
        return {
            'score': float(score),
            'roc': float(roc),
            'roc_normalized': float(roc_normalized),
            'slope': float(slope),
            'annualized_return': float(((1 + slope) ** 252 - 1) * 100)
        }
    except Exception as e:
        print(f"Error calculating momentum: {e}")
        return None

def calculate_portfolio_metrics(returns: pd.Series) -> Dict:
    """
    Calculate portfolio performance metrics
    
    Args:
        returns: Series of daily returns
    
    Returns:
        Dictionary with performance metrics
    """
    if len(returns) == 0:
        return {}
    
    try:
        total_return = (1 + returns).prod() - 1
        annual_return = (1 + total_return) ** (252 / len(returns)) - 1
        volatility = returns.std() * np.sqrt(252)
        sharpe_ratio = annual_return / volatility if volatility > 0 else 0
        
        # Maximum drawdown
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        return {
            'total_return': float(total_return * 100),
            'annual_return': float(annual_return * 100),
            'volatility': float(volatility * 100),
            'sharpe_ratio': float(sharpe_ratio),
            'max_drawdown': float(max_drawdown * 100),
            'num_periods': len(returns)
        }
    except Exception as e:
        print(f"Error calculating metrics: {e}")
        return {}

def get_sp500_tickers() -> List[str]:
    """Get S&P 500 tickers from Wikipedia"""
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        tables = pd.read_html(url)
        df = tables[0]
        tickers = df['Symbol'].tolist()
        # Clean tickers for yfinance
        tickers = [t.replace('.', '-') for t in tickers]
        return tickers
    except Exception as e:
        print(f"Error fetching S&P 500 tickers: {e}")
        return []

def get_nasdaq100_tickers() -> List[str]:
    """Get NASDAQ-100 tickers from Wikipedia"""
    try:
        url = 'https://en.wikipedia.org/wiki/NASDAQ-100'
        tables = pd.read_html(url)
        df = tables[4]  # The constituents table
        tickers = df['Ticker'].tolist()
        return tickers
    except Exception as e:
        print(f"Error fetching NASDAQ-100 tickers: {e}")
        return []

def simple_backtest(prices: pd.DataFrame, lookback: int = 200, roc_period: int = 200, 
                   rebalance_days: int = 14, top_n: int = 1, initial_capital: float = 100000) -> Dict:
    """
    Simple momentum backtest
    
    Args:
        prices: DataFrame with tickers as columns, dates as index
        lookback: Lookback period for trend
        roc_period: ROC calculation period
        rebalance_days: Days between rebalances
        top_n: Number of top stocks to hold
        initial_capital: Starting capital
    
    Returns:
        Dictionary with backtest results
    """
    if prices.empty or len(prices) < max(lookback, roc_period):
        return {}
    
    try:
        portfolio_value = [initial_capital]
        dates = []
        holdings = []
        
        # Start after warmup period
        start_idx = max(lookback, roc_period)
        
        for i in range(start_idx, len(prices), rebalance_days):
            current_date = prices.index[i]
            dates.append(current_date)
            
            # Calculate momentum for all stocks
            scores = {}
            for ticker in prices.columns:
                momentum = calculate_momentum_score(prices[ticker].iloc[:i], lookback, roc_period)
                if momentum and momentum['score'] > 0:
                    scores[ticker] = momentum['score']
            
            if not scores:
                portfolio_value.append(portfolio_value[-1])
                holdings.append([])
                continue
            
            # Select top N
            top_stocks = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
            selected = [ticker for ticker, _ in top_stocks]
            holdings.append(selected)
            
            # Calculate returns until next rebalance
            next_idx = min(i + rebalance_days, len(prices) - 1)
            period_returns = []
            
            for ticker in selected:
                start_price = prices[ticker].iloc[i]
                end_price = prices[ticker].iloc[next_idx]
                if start_price > 0:
                    ret = (end_price - start_price) / start_price
                    period_returns.append(ret)
            
            if period_returns:
                avg_return = np.mean(period_returns)
                portfolio_value.append(portfolio_value[-1] * (1 + avg_return))
            else:
                portfolio_value.append(portfolio_value[-1])
        
        # Calculate metrics
        returns = pd.Series(portfolio_value).pct_change().dropna()
        metrics = calculate_portfolio_metrics(returns)
        
        return {
            'portfolio_value': portfolio_value,
            'dates': dates,
            'holdings': holdings,
            'metrics': metrics,
            'final_value': portfolio_value[-1],
            'total_return': ((portfolio_value[-1] - initial_capital) / initial_capital) * 100
        }
    except Exception as e:
        print(f"Error in backtest: {e}")
        return {}
