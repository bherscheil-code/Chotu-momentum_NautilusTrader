"""
Advanced Trading Strategies - Integrated from all Chotu projects
Combines:
1. Momentum TAA (from Chotu-qstrader)
2. Indicator-based algo (from Chotu-stock-analysis-engine)
3. ROC × Trend Slope (from root momentum files)
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import operator

# ============================================================================
# STRATEGY 1: Top-N Momentum TAA (from Chotu-qstrader/examples/momentum_taa.py)
# ============================================================================

class TopNMomentumStrategy:
    """
    Tactical Asset Allocation using momentum
    Selects top N assets by momentum score
    """
    
    def __init__(self, lookback: int = 126, top_n: int = 3):
        """
        Parameters:
        - lookback: Days for momentum calculation (126 = 6 months)
        - top_n: Number of top assets to hold
        """
        self.lookback = lookback
        self.top_n = top_n
        self.name = f"TopN_Momentum_{lookback}d_Top{top_n}"
    
    def calculate_momentum(self, prices: pd.Series) -> float:
        """Calculate holding-period return momentum"""
        if len(prices) < self.lookback:
            return np.nan
        
        current = prices.iloc[-1]
        past = prices.iloc[-self.lookback]
        
        if past == 0 or np.isnan(past) or np.isnan(current):
            return np.nan
        
        # Holding period return
        momentum = (current - past) / past
        return momentum
    
    def select_top_assets(self, prices_df: pd.DataFrame) -> List[str]:
        """
        Select top N assets by momentum
        
        Parameters:
        - prices_df: DataFrame with tickers as columns, dates as index
        
        Returns:
        - List of top N ticker symbols
        """
        momenta = {}
        
        for ticker in prices_df.columns:
            mom = self.calculate_momentum(prices_df[ticker])
            if not np.isnan(mom):
                momenta[ticker] = mom
        
        # Sort by momentum descending
        sorted_assets = sorted(
            momenta.items(),
            key=operator.itemgetter(1),
            reverse=True
        )
        
        # Return top N
        return [asset[0] for asset in sorted_assets[:self.top_n]]
    
    def generate_weights(self, prices_df: pd.DataFrame) -> Dict[str, float]:
        """
        Generate equal-weight allocations for top N assets
        
        Returns:
        - Dictionary of {ticker: weight}
        """
        top_assets = self.select_top_assets(prices_df)
        
        weights = {ticker: 0.0 for ticker in prices_df.columns}
        
        if len(top_assets) > 0:
            weight_per_asset = 1.0 / len(top_assets)
            for asset in top_assets:
                weights[asset] = weight_per_asset
        
        return weights


# ============================================================================
# STRATEGY 2: 60/40 Portfolio (from Chotu-qstrader/examples/sixty_forty.py)
# ============================================================================

class SixtyFortyStrategy:
    """
    Classic 60% stocks / 40% bonds portfolio
    Rebalanced monthly
    """
    
    def __init__(self, stock_weight: float = 0.6, bond_weight: float = 0.4):
        """
        Parameters:
        - stock_weight: Allocation to stocks (default 60%)
        - bond_weight: Allocation to bonds (default 40%)
        """
        self.stock_weight = stock_weight
        self.bond_weight = bond_weight
        self.name = f"{int(stock_weight*100)}/{int(bond_weight*100)}_Portfolio"
    
    def generate_weights(self, stock_ticker: str = 'SPY', bond_ticker: str = 'AGG') -> Dict[str, float]:
        """
        Generate fixed allocations
        
        Returns:
        - Dictionary of {ticker: weight}
        """
        return {
            stock_ticker: self.stock_weight,
            bond_ticker: self.bond_weight
        }


# ============================================================================
# STRATEGY 3: ROC × Trend Slope Momentum (from root momentum files)
# ============================================================================

class ROCTrendMomentumStrategy:
    """
    Advanced momentum using ROC × Trend Slope
    From proven NautilusTrader backtests
    """
    
    def __init__(self, lookback: int = 200, roc_period: int = 200, top_n: int = 1):
        """
        Parameters:
        - lookback: Days for trend slope calculation
        - roc_period: Days for ROC calculation
        - top_n: Number of top stocks to hold
        """
        self.lookback = lookback
        self.roc_period = roc_period
        self.top_n = top_n
        self.name = f"ROC_Trend_L{lookback}_R{roc_period}_Top{top_n}"
    
    def calculate_momentum_score(self, prices: pd.Series) -> float:
        """
        Calculate momentum score: ROC × Trend Slope
        
        Returns:
        - Momentum score (higher = stronger momentum)
        """
        if len(prices) < max(self.lookback, self.roc_period):
            return np.nan
        
        # ROC calculation
        current_price = prices.iloc[-1]
        past_price = prices.iloc[-self.roc_period]
        
        if past_price <= 0 or np.isnan(past_price) or np.isnan(current_price):
            return np.nan
        
        roc = ((current_price - past_price) / past_price) * 100
        roc_normalized = max(0, min(1, float(np.ceil(roc))))
        
        # Trend slope calculation
        recent_prices = prices.tail(self.lookback)
        log_prices = np.log(recent_prices.replace(0, np.nan).dropna())
        
        if len(log_prices) < 20:
            return np.nan
        
        x = np.arange(len(log_prices))
        slope = np.polyfit(x, log_prices, 1)[0]
        
        # Combined momentum score
        score = roc_normalized * slope
        
        if not np.isfinite(score):
            return np.nan
        
        return float(score)
    
    def select_top_assets(self, prices_df: pd.DataFrame) -> List[str]:
        """
        Select top N assets by momentum score
        
        Parameters:
        - prices_df: DataFrame with tickers as columns, dates as index
        
        Returns:
        - List of top N ticker symbols
        """
        scores = {}
        
        for ticker in prices_df.columns:
            score = self.calculate_momentum_score(prices_df[ticker])
            if not np.isnan(score) and score > 0:  # Only positive momentum
                scores[ticker] = score
        
        # Sort by score descending
        sorted_assets = sorted(
            scores.items(),
            key=operator.itemgetter(1),
            reverse=True
        )
        
        # Return top N
        return [asset[0] for asset in sorted_assets[:self.top_n]]
    
    def generate_weights(self, prices_df: pd.DataFrame) -> Dict[str, float]:
        """
        Generate equal-weight allocations for top N assets
        
        Returns:
        - Dictionary of {ticker: weight}
        """
        top_assets = self.select_top_assets(prices_df)
        
        weights = {ticker: 0.0 for ticker in prices_df.columns}
        
        if len(top_assets) > 0:
            weight_per_asset = 1.0 / len(top_assets)
            for asset in top_assets:
                weights[asset] = weight_per_asset
        
        return weights


# ============================================================================
# STRATEGY 4: Indicator-Based Algo (from Chotu-stock-analysis-engine)
# ============================================================================

class IndicatorBasedStrategy:
    """
    Multi-indicator strategy with buy/sell rules
    Inspired by Chotu-stock-analysis-engine/analysis_engine/algo.py
    """
    
    def __init__(self, min_buy_indicators: int = 2, min_sell_indicators: int = 2):
        """
        Parameters:
        - min_buy_indicators: Minimum indicators saying buy to trigger
        - min_sell_indicators: Minimum indicators saying sell to trigger
        """
        self.min_buy_indicators = min_buy_indicators
        self.min_sell_indicators = min_sell_indicators
        self.name = f"Indicator_Buy{min_buy_indicators}_Sell{min_sell_indicators}"
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> float:
        """Calculate RSI indicator"""
        if len(prices) < period + 1:
            return 50.0  # Neutral
        
        deltas = prices.diff()
        gains = deltas.where(deltas > 0, 0)
        losses = -deltas.where(deltas < 0, 0)
        
        avg_gain = gains.rolling(window=period).mean().iloc[-1]
        avg_loss = losses.rolling(window=period).mean().iloc[-1]
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def calculate_macd(self, prices: pd.Series) -> Tuple[float, float]:
        """Calculate MACD indicator"""
        if len(prices) < 26:
            return 0.0, 0.0
        
        ema12 = prices.ewm(span=12, adjust=False).mean().iloc[-1]
        ema26 = prices.ewm(span=26, adjust=False).mean().iloc[-1]
        macd = ema12 - ema26
        
        macd_series = prices.ewm(span=12, adjust=False).mean() - prices.ewm(span=26, adjust=False).mean()
        signal = macd_series.ewm(span=9, adjust=False).mean().iloc[-1]
        
        return macd, signal
    
    def calculate_moving_average_cross(self, prices: pd.Series) -> str:
        """Check if short MA crossed above/below long MA"""
        if len(prices) < 50:
            return 'neutral'
        
        ma20 = prices.rolling(window=20).mean().iloc[-1]
        ma50 = prices.rolling(window=50).mean().iloc[-1]
        
        if ma20 > ma50:
            return 'bullish'
        elif ma20 < ma50:
            return 'bearish'
        else:
            return 'neutral'
    
    def generate_signals(self, prices: pd.Series) -> Dict[str, any]:
        """
        Generate buy/sell signals based on multiple indicators
        
        Returns:
        - Dictionary with signals and indicator values
        """
        # Calculate indicators
        rsi = self.calculate_rsi(prices)
        macd, signal = self.calculate_macd(prices)
        ma_cross = self.calculate_moving_average_cross(prices)
        
        # Buy/sell logic
        buy_signals = []
        sell_signals = []
        
        # RSI signals
        if rsi < 30:
            buy_signals.append('RSI_oversold')
        elif rsi > 70:
            sell_signals.append('RSI_overbought')
        
        # MACD signals
        if macd > signal:
            buy_signals.append('MACD_bullish')
        elif macd < signal:
            sell_signals.append('MACD_bearish')
        
        # MA cross signals
        if ma_cross == 'bullish':
            buy_signals.append('MA_cross_bullish')
        elif ma_cross == 'bearish':
            sell_signals.append('MA_cross_bearish')
        
        # Decision
        action = 'hold'
        if len(buy_signals) >= self.min_buy_indicators:
            action = 'buy'
        elif len(sell_signals) >= self.min_sell_indicators:
            action = 'sell'
        
        return {
            'action': action,
            'buy_signals': buy_signals,
            'sell_signals': sell_signals,
            'num_buy': len(buy_signals),
            'num_sell': len(sell_signals),
            'rsi': rsi,
            'macd': macd,
            'macd_signal': signal,
            'ma_cross': ma_cross
        }


# ============================================================================
# STRATEGY COMPARISON FRAMEWORK
# ============================================================================

class StrategyComparison:
    """
    Compare multiple strategies on the same data
    """
    
    def __init__(self, strategies: List):
        """
        Parameters:
        - strategies: List of strategy objects
        """
        self.strategies = strategies
    
    def backtest_all(self, prices_df: pd.DataFrame, rebalance_freq: int = 21) -> pd.DataFrame:
        """
        Backtest all strategies
        
        Parameters:
        - prices_df: DataFrame with tickers as columns, dates as index
        - rebalance_freq: Days between rebalances
        
        Returns:
        - DataFrame with strategy performance
        """
        results = []
        
        for strategy in self.strategies:
            # Simple backtest
            portfolio_values = [100000]  # Start with $100k
            
            for i in range(max(strategy.lookback if hasattr(strategy, 'lookback') else 200, 200), 
                          len(prices_df), rebalance_freq):
                
                # Get weights
                historical_prices = prices_df.iloc[:i]
                
                if hasattr(strategy, 'generate_weights'):
                    weights = strategy.generate_weights(historical_prices)
                else:
                    weights = {ticker: 0.0 for ticker in prices_df.columns}
                
                # Calculate returns
                if i + rebalance_freq < len(prices_df):
                    period_returns = []
                    for ticker, weight in weights.items():
                        if weight > 0 and ticker in prices_df.columns:
                            start_price = prices_df[ticker].iloc[i]
                            end_price = prices_df[ticker].iloc[min(i + rebalance_freq, len(prices_df) - 1)]
                            if start_price > 0:
                                ret = (end_price - start_price) / start_price
                                period_returns.append(weight * ret)
                    
                    if period_returns:
                        portfolio_return = sum(period_returns)
                        portfolio_values.append(portfolio_values[-1] * (1 + portfolio_return))
            
            # Calculate metrics
            total_return = ((portfolio_values[-1] - portfolio_values[0]) / portfolio_values[0]) * 100
            
            results.append({
                'Strategy': strategy.name,
                'Final Value': portfolio_values[-1],
                'Total Return %': total_return,
                'Num Rebalances': len(portfolio_values) - 1
            })
        
        return pd.DataFrame(results).sort_values('Total Return %', ascending=False)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_all_strategies() -> List:
    """
    Get all available strategies
    
    Returns:
    - List of strategy objects
    """
    return [
        TopNMomentumStrategy(lookback=126, top_n=3),
        TopNMomentumStrategy(lookback=252, top_n=1),
        SixtyFortyStrategy(),
        ROCTrendMomentumStrategy(lookback=200, roc_period=200, top_n=1),
        ROCTrendMomentumStrategy(lookback=150, roc_period=150, top_n=3),
        IndicatorBasedStrategy(min_buy_indicators=2, min_sell_indicators=2)
    ]


def get_strategy_descriptions() -> Dict[str, str]:
    """
    Get descriptions of all strategies
    
    Returns:
    - Dictionary of {strategy_name: description}
    """
    return {
        'Top-N Momentum TAA': 'Tactical Asset Allocation selecting top N assets by holding-period return momentum (from Chotu-qstrader)',
        '60/40 Portfolio': 'Classic balanced portfolio with 60% stocks, 40% bonds (from Chotu-qstrader)',
        'ROC × Trend Slope': 'Advanced momentum combining Rate of Change with trend slope analysis (from root momentum files)',
        'Indicator-Based': 'Multi-indicator strategy using RSI, MACD, and moving averages (from Chotu-stock-analysis-engine)'
    }
