"""
Technical Indicators Module
Complete integration from Chotu-stock-analysis-engine
Includes: RSI, MACD, Bollinger Bands, Stochastic, Williams %R, OBV, ROC, and more
"""
import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple

class TechnicalIndicators:
    """
    Comprehensive technical analysis indicators
    From Chotu-stock-analysis-engine/analysis_engine/indicators/
    """
    
    @staticmethod
    def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
        """
        Relative Strength Index (RSI)
        Measures momentum, overbought/oversold conditions
        
        Returns: Series with RSI values (0-100)
        - Above 70: Overbought
        - Below 30: Oversold
        """
        if len(prices) < period + 1:
            return pd.Series([50.0] * len(prices), index=prices.index)
        
        deltas = prices.diff()
        gains = deltas.where(deltas > 0, 0)
        losses = -deltas.where(deltas < 0, 0)
        
        avg_gain = gains.rolling(window=period).mean()
        avg_loss = losses.rolling(window=period).mean()
        
        rs = avg_gain / avg_loss.replace(0, np.nan)
        rsi = 100 - (100 / (1 + rs))
        
        return rsi.fillna(50)
    
    @staticmethod
    def calculate_macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Moving Average Convergence Divergence (MACD)
        Trend-following momentum indicator
        
        Returns: (macd_line, signal_line, histogram)
        - MACD > Signal: Bullish
        - MACD < Signal: Bearish
        """
        if len(prices) < slow:
            empty = pd.Series([0.0] * len(prices), index=prices.index)
            return empty, empty, empty
        
        ema_fast = prices.ewm(span=fast, adjust=False).mean()
        ema_slow = prices.ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    @staticmethod
    def calculate_bollinger_bands(prices: pd.Series, period: int = 20, std_dev: float = 2.0) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Bollinger Bands
        Volatility indicator
        
        Returns: (upper_band, middle_band, lower_band)
        - Price near upper: Overbought
        - Price near lower: Oversold
        """
        if len(prices) < period:
            middle = pd.Series([prices.mean()] * len(prices), index=prices.index)
            return middle, middle, middle
        
        middle_band = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper_band = middle_band + (std * std_dev)
        lower_band = middle_band - (std * std_dev)
        
        return upper_band, middle_band, lower_band
    
    @staticmethod
    def calculate_stochastic(high: pd.Series, low: pd.Series, close: pd.Series, 
                            k_period: int = 14, d_period: int = 3) -> Tuple[pd.Series, pd.Series]:
        """
        Stochastic Oscillator
        Momentum indicator comparing closing price to price range
        
        Returns: (%K, %D)
        - Above 80: Overbought
        - Below 20: Oversold
        """
        if len(close) < k_period:
            empty = pd.Series([50.0] * len(close), index=close.index)
            return empty, empty
        
        lowest_low = low.rolling(window=k_period).min()
        highest_high = high.rolling(window=k_period).max()
        
        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low).replace(0, np.nan))
        d_percent = k_percent.rolling(window=d_period).mean()
        
        return k_percent.fillna(50), d_percent.fillna(50)
    
    @staticmethod
    def calculate_williams_r(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """
        Williams %R
        Momentum indicator (similar to Stochastic but inverted)
        
        Returns: Series with Williams %R values (-100 to 0)
        - Above -20: Overbought
        - Below -80: Oversold
        """
        if len(close) < period:
            return pd.Series([-50.0] * len(close), index=close.index)
        
        highest_high = high.rolling(window=period).max()
        lowest_low = low.rolling(window=period).min()
        
        williams_r = -100 * ((highest_high - close) / (highest_high - lowest_low).replace(0, np.nan))
        
        return williams_r.fillna(-50)
    
    @staticmethod
    def calculate_obv(close: pd.Series, volume: pd.Series) -> pd.Series:
        """
        On-Balance Volume (OBV)
        Volume-based momentum indicator
        
        Returns: Series with cumulative OBV
        - Rising OBV: Buying pressure
        - Falling OBV: Selling pressure
        """
        if len(close) < 2:
            return pd.Series([0.0] * len(close), index=close.index)
        
        obv = pd.Series(index=close.index, dtype=float)
        obv.iloc[0] = volume.iloc[0]
        
        for i in range(1, len(close)):
            if close.iloc[i] > close.iloc[i-1]:
                obv.iloc[i] = obv.iloc[i-1] + volume.iloc[i]
            elif close.iloc[i] < close.iloc[i-1]:
                obv.iloc[i] = obv.iloc[i-1] - volume.iloc[i]
            else:
                obv.iloc[i] = obv.iloc[i-1]
        
        return obv
    
    @staticmethod
    def calculate_roc(prices: pd.Series, period: int = 12) -> pd.Series:
        """
        Rate of Change (ROC)
        Momentum indicator measuring percentage change
        
        Returns: Series with ROC values
        - Positive: Upward momentum
        - Negative: Downward momentum
        """
        if len(prices) < period + 1:
            return pd.Series([0.0] * len(prices), index=prices.index)
        
        roc = ((prices - prices.shift(period)) / prices.shift(period).replace(0, np.nan)) * 100
        
        return roc.fillna(0)
    
    @staticmethod
    def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """
        Average True Range (ATR)
        Volatility indicator
        
        Returns: Series with ATR values
        - Higher ATR: More volatile
        - Lower ATR: Less volatile
        """
        if len(close) < 2:
            return pd.Series([0.0] * len(close), index=close.index)
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = true_range.rolling(window=period).mean()
        
        return atr.fillna(0)
    
    @staticmethod
    def calculate_adx(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """
        Average Directional Index (ADX)
        Trend strength indicator
        
        Returns: Series with ADX values (0-100)
        - Above 25: Strong trend
        - Below 20: Weak trend
        """
        if len(close) < period + 1:
            return pd.Series([20.0] * len(close), index=close.index)
        
        # Calculate +DM and -DM
        high_diff = high.diff()
        low_diff = -low.diff()
        
        plus_dm = high_diff.where((high_diff > low_diff) & (high_diff > 0), 0)
        minus_dm = low_diff.where((low_diff > high_diff) & (low_diff > 0), 0)
        
        # Calculate ATR
        atr = TechnicalIndicators.calculate_atr(high, low, close, period)
        
        # Calculate +DI and -DI
        plus_di = 100 * (plus_dm.rolling(window=period).mean() / atr.replace(0, np.nan))
        minus_di = 100 * (minus_dm.rolling(window=period).mean() / atr.replace(0, np.nan))
        
        # Calculate DX and ADX
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di).replace(0, np.nan)
        adx = dx.rolling(window=period).mean()
        
        return adx.fillna(20)
    
    @staticmethod
    def calculate_cci(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 20) -> pd.Series:
        """
        Commodity Channel Index (CCI)
        Momentum indicator
        
        Returns: Series with CCI values
        - Above +100: Overbought
        - Below -100: Oversold
        """
        if len(close) < period:
            return pd.Series([0.0] * len(close), index=close.index)
        
        typical_price = (high + low + close) / 3
        sma = typical_price.rolling(window=period).mean()
        mean_deviation = typical_price.rolling(window=period).apply(lambda x: abs(x - x.mean()).mean())
        
        cci = (typical_price - sma) / (0.015 * mean_deviation.replace(0, np.nan))
        
        return cci.fillna(0)
    
    @staticmethod
    def calculate_mfi(high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, period: int = 14) -> pd.Series:
        """
        Money Flow Index (MFI)
        Volume-weighted RSI
        
        Returns: Series with MFI values (0-100)
        - Above 80: Overbought
        - Below 20: Oversold
        """
        if len(close) < period + 1:
            return pd.Series([50.0] * len(close), index=close.index)
        
        typical_price = (high + low + close) / 3
        money_flow = typical_price * volume
        
        positive_flow = money_flow.where(typical_price > typical_price.shift(), 0)
        negative_flow = money_flow.where(typical_price < typical_price.shift(), 0)
        
        positive_mf = positive_flow.rolling(window=period).sum()
        negative_mf = negative_flow.rolling(window=period).sum()
        
        mfi = 100 - (100 / (1 + positive_mf / negative_mf.replace(0, np.nan)))
        
        return mfi.fillna(50)


class AdvancedTechnicalAnalysis:
    """
    Advanced technical analysis combining multiple indicators
    From Chotu-stock-analysis-engine algo.py logic
    """
    
    def __init__(self, min_buy_indicators: int = 3, min_sell_indicators: int = 3):
        """
        Parameters:
        - min_buy_indicators: Minimum indicators saying buy to trigger
        - min_sell_indicators: Minimum indicators saying sell to trigger
        """
        self.min_buy_indicators = min_buy_indicators
        self.min_sell_indicators = min_sell_indicators
        self.indicators = TechnicalIndicators()
    
    def analyze_stock(self, df: pd.DataFrame) -> Dict:
        """
        Comprehensive technical analysis
        
        Parameters:
        - df: DataFrame with OHLCV data (Open, High, Low, Close, Volume)
        
        Returns:
        - Dictionary with all indicators and signals
        """
        if len(df) < 50:
            return {'error': 'Not enough data (need at least 50 bars)'}
        
        close = df['Close']
        high = df['High']
        low = df['Low']
        volume = df['Volume']
        
        # Calculate all indicators
        rsi = self.indicators.calculate_rsi(close)
        macd_line, signal_line, histogram = self.indicators.calculate_macd(close)
        upper_bb, middle_bb, lower_bb = self.indicators.calculate_bollinger_bands(close)
        k_percent, d_percent = self.indicators.calculate_stochastic(high, low, close)
        williams_r = self.indicators.calculate_williams_r(high, low, close)
        obv = self.indicators.calculate_obv(close, volume)
        roc = self.indicators.calculate_roc(close)
        atr = self.indicators.calculate_atr(high, low, close)
        adx = self.indicators.calculate_adx(high, low, close)
        cci = self.indicators.calculate_cci(high, low, close)
        mfi = self.indicators.calculate_mfi(high, low, close, volume)
        
        # Get latest values
        latest = {
            'rsi': rsi.iloc[-1],
            'macd': macd_line.iloc[-1],
            'macd_signal': signal_line.iloc[-1],
            'macd_histogram': histogram.iloc[-1],
            'bb_upper': upper_bb.iloc[-1],
            'bb_middle': middle_bb.iloc[-1],
            'bb_lower': lower_bb.iloc[-1],
            'stoch_k': k_percent.iloc[-1],
            'stoch_d': d_percent.iloc[-1],
            'williams_r': williams_r.iloc[-1],
            'obv': obv.iloc[-1],
            'roc': roc.iloc[-1],
            'atr': atr.iloc[-1],
            'adx': adx.iloc[-1],
            'cci': cci.iloc[-1],
            'mfi': mfi.iloc[-1],
            'price': close.iloc[-1]
        }
        
        # Generate signals
        buy_signals = []
        sell_signals = []
        
        # RSI signals
        if latest['rsi'] < 30:
            buy_signals.append('RSI_oversold')
        elif latest['rsi'] > 70:
            sell_signals.append('RSI_overbought')
        
        # MACD signals
        if latest['macd'] > latest['macd_signal'] and latest['macd_histogram'] > 0:
            buy_signals.append('MACD_bullish')
        elif latest['macd'] < latest['macd_signal'] and latest['macd_histogram'] < 0:
            sell_signals.append('MACD_bearish')
        
        # Bollinger Bands signals
        if latest['price'] < latest['bb_lower']:
            buy_signals.append('BB_oversold')
        elif latest['price'] > latest['bb_upper']:
            sell_signals.append('BB_overbought')
        
        # Stochastic signals
        if latest['stoch_k'] < 20 and latest['stoch_d'] < 20:
            buy_signals.append('STOCH_oversold')
        elif latest['stoch_k'] > 80 and latest['stoch_d'] > 80:
            sell_signals.append('STOCH_overbought')
        
        # Williams %R signals
        if latest['williams_r'] < -80:
            buy_signals.append('WILLR_oversold')
        elif latest['williams_r'] > -20:
            sell_signals.append('WILLR_overbought')
        
        # ROC signals
        if latest['roc'] > 5:
            buy_signals.append('ROC_positive')
        elif latest['roc'] < -5:
            sell_signals.append('ROC_negative')
        
        # ADX signals (trend strength)
        trend_strength = 'strong' if latest['adx'] > 25 else 'weak'
        
        # CCI signals
        if latest['cci'] < -100:
            buy_signals.append('CCI_oversold')
        elif latest['cci'] > 100:
            sell_signals.append('CCI_overbought')
        
        # MFI signals
        if latest['mfi'] < 20:
            buy_signals.append('MFI_oversold')
        elif latest['mfi'] > 80:
            sell_signals.append('MFI_overbought')
        
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
            'trend_strength': trend_strength,
            'indicators': latest,
            'series': {
                'rsi': rsi,
                'macd': macd_line,
                'macd_signal': signal_line,
                'bb_upper': upper_bb,
                'bb_middle': middle_bb,
                'bb_lower': lower_bb,
                'stoch_k': k_percent,
                'stoch_d': d_percent
            }
        }
