"""
Stock Learning Hub - Integrated Educational Platform
Combines momentum strategy, backtesting, and live analysis for learning stock investment
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import yfinance as yf
from pathlib import Path
import sys

# Add parent directory for imports
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent))

# Import advanced strategies
try:
    from advanced_strategies import (
        TopNMomentumStrategy,
        SixtyFortyStrategy,
        ROCTrendMomentumStrategy,
        IndicatorBasedStrategy,
        StrategyComparison,
        get_all_strategies,
        get_strategy_descriptions
    )
    ADVANCED_STRATEGIES_AVAILABLE = True
except ImportError:
    ADVANCED_STRATEGIES_AVAILABLE = False

# Import user manual
try:
    from user_manual import show_user_manual
    USER_MANUAL_AVAILABLE = True
except ImportError:
    USER_MANUAL_AVAILABLE = False

# Import technical indicators
try:
    from technical_indicators import TechnicalIndicators, AdvancedTechnicalAnalysis
    from technical_analysis_module import show_technical_analysis
    TECHNICAL_INDICATORS_AVAILABLE = True
except ImportError:
    TECHNICAL_INDICATORS_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Stock Learning Hub",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
    .feature-card {
        padding: 1.5rem;
        border-radius: 10px;
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Utility functions
@st.cache_data(ttl=3600)
def get_stock_data(ticker, period="1y"):
    """Fetch stock data with caching"""
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        return df
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

def calculate_momentum_score(prices, lookback=200, roc_period=200):
    """Calculate momentum score: ROC × Trend Slope"""
    if len(prices) < max(lookback, roc_period):
        return None
    
    # ROC calculation
    current_price = prices.iloc[-1]
    past_price = prices.iloc[-roc_period]
    roc = ((current_price - past_price) / past_price) * 100
    roc_normalized = max(0, min(1, np.ceil(roc)))
    
    # Trend slope calculation
    recent_prices = prices.tail(lookback)
    log_prices = np.log(recent_prices.replace(0, np.nan).dropna())
    
    if len(log_prices) < 20:
        return None
    
    x = np.arange(len(log_prices))
    slope = np.polyfit(x, log_prices, 1)[0]
    
    # Momentum score
    score = roc_normalized * slope
    
    return {
        'score': score,
        'roc': roc,
        'roc_normalized': roc_normalized,
        'slope': slope,
        'annualized_return': ((1 + slope) ** 252 - 1) * 100
    }

def plot_price_chart(df, ticker):
    """Create interactive price chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name=ticker
    ))
    
    # Add moving averages
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['MA200'] = df['Close'].rolling(window=200).mean()
    
    fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], name='MA50', line=dict(color='orange', width=1)))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA200'], name='MA200', line=dict(color='red', width=1)))
    
    fig.update_layout(
        title=f'{ticker} Price Chart',
        yaxis_title='Price ($)',
        xaxis_title='Date',
        template='plotly_white',
        height=500
    )
    
    return fig

# Main app
def main():
    st.markdown('<h1 class="main-header">📚 Stock Learning Hub</h1>', unsafe_allow_html=True)
    st.markdown("### Learn Stock Investment Through Interactive Analysis")
    
    # Sidebar navigation
    st.sidebar.title("📚 Navigation")
    page = st.sidebar.radio(
        "Choose a module:",
        [
            "🏠 Home",
            "📖 Learn: Stock Basics",
            "🎯 Momentum Strategy",
            "📊 Live Market Analysis",
            "📈 Technical Analysis",
            "🔬 Backtest Simulator",
            "🚀 Advanced Strategies",
            "⚔️ Strategy Comparison",
            "📚 User Manual",
            "🎮 Paper Trading",
            "📊 Portfolio Tracker"
        ]
    )
    
    if page == "🏠 Home":
        show_home()
    elif page == "📖 Learn: Stock Basics":
        show_learning_module()
    elif page == "🎯 Momentum Strategy":
        show_momentum_strategy()
    elif page == "📊 Live Market Analysis":
        show_live_analysis()
    elif page == "📈 Technical Analysis":
        if TECHNICAL_INDICATORS_AVAILABLE:
            show_technical_analysis()
        else:
            st.error("Technical analysis module not available.")
            st.info("Please ensure technical_indicators.py and technical_analysis_module.py are in the same directory")
    elif page == "🔬 Backtest Simulator":
        show_backtest()
    elif page == "🚀 Advanced Strategies":
        show_advanced_strategies()
    elif page == "⚔️ Strategy Comparison":
        show_strategy_comparison()
    elif page == "📚 User Manual":
        if USER_MANUAL_AVAILABLE:
            show_user_manual()
        else:
            st.error("User manual module not available.")
            st.info("Please ensure user_manual.py is in the same directory as app.py")
    elif page == "🎮 Paper Trading":
        show_paper_trading()
    elif page == "📊 Portfolio Tracker":
        show_portfolio()

def show_home():
    """Home page with overview"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2>📖</h2>
            <h3>Learn</h3>
            <p>Stock market fundamentals</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>🔬</h2>
            <h3>Practice</h3>
            <p>Backtest strategies safely</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2>📈</h2>
            <h3>Analyze</h3>
            <p>Real-time market insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    ## 🎯 What You'll Learn
    
    This platform combines proven strategies from professional trading systems to teach you:
    
    ### 1. Momentum Strategy
    - Understand how to identify trending stocks
    - Learn the ROC (Rate of Change) + Trend Slope methodology
    - See real examples from S&P 500, NASDAQ-100, and global indices
    
    ### 2. Risk Management
    - Position sizing and capital allocation
    - Drawdown analysis and recovery
    - Portfolio diversification principles
    
    ### 3. Backtesting
    - Test strategies on historical data
    - Understand performance metrics (Sharpe ratio, max drawdown)
    - Learn what works and what doesn't
    
    ### 4. Live Analysis
    - Real-time momentum scoring
    - Compare stocks across indices
    - Track market trends
    
    ## 🚀 Getting Started
    
    1. **Start with "Learn: Stock Basics"** to understand fundamental concepts
    2. **Explore "Momentum Strategy"** to see how systematic trading works
    3. **Try "Live Market Analysis"** to analyze real stocks
    4. **Use "Backtest Simulator"** to test ideas safely
    5. **Practice with "Paper Trading"** before risking real money
    
    ## ⚠️ Important Disclaimer
    
    This is an **educational platform**. Always remember:
    - Past performance doesn't guarantee future results
    - Start with paper trading before using real money
    - Never invest more than you can afford to lose
    - Consult financial advisors for personalized advice
    """)

def show_learning_module():
    """Educational content about stock investing"""
    st.header("📖 Stock Investment Basics")
    
    tab1, tab2, tab3, tab4 = st.tabs(["What are Stocks?", "Momentum Strategy", "Risk Management", "Key Metrics"])
    
    with tab1:
        st.markdown("""
        ## What are Stocks?
        
        Stocks represent ownership in a company. When you buy a stock, you become a partial owner of that business.
        
        ### Why Do Stock Prices Move?
        
        Stock prices change based on:
        - **Company Performance**: Earnings, revenue, growth
        - **Market Sentiment**: Investor confidence and emotions
        - **Economic Factors**: Interest rates, inflation, GDP
        - **Supply & Demand**: More buyers = price up, more sellers = price down
        
        ### Types of Analysis
        
        1. **Fundamental Analysis**: Evaluating company financials, management, competitive advantage
        2. **Technical Analysis**: Using price patterns, trends, and indicators
        3. **Quantitative Analysis**: Using mathematical models and statistics (what we focus on)
        
        ### Stock Indices
        
        - **S&P 500**: 500 largest US companies
        - **NASDAQ-100**: 100 largest non-financial companies on NASDAQ
        - **DAX40**: 40 largest German companies
        - **NIFTY50**: 50 largest Indian companies
        """)
    
    with tab2:
        st.markdown("""
        ## Momentum Strategy Explained
        
        Momentum investing is based on the principle: **"What goes up tends to keep going up"**
        
        ### Our Momentum Formula
        
        We use two components to calculate momentum:
        
        #### 1. ROC (Rate of Change)
        ```
        ROC = ((Current Price - Past Price) / Past Price) × 100
        ```
        - Measures percentage change over time
        - Normalized to 0-1 range for consistency
        
        #### 2. Trend Slope
        ```
        Slope = Linear regression on log(prices) over lookback period
        ```
        - Measures the strength and direction of the trend
        - Positive slope = uptrend, negative = downtrend
        
        #### 3. Momentum Score
        ```
        Momentum Score = ROC × Trend Slope
        ```
        - Combines both rate of change and trend strength
        - Higher score = stronger momentum
        
        ### Why This Works
        
        - **Trend Following**: Captures sustained price movements
        - **Objective**: No emotions, just math
        - **Systematic**: Can be backtested and optimized
        - **Risk-Aware**: Avoids stocks in downtrends
        
        ### When It Doesn't Work
        
        - **Mean-Reverting Markets**: When prices bounce back quickly
        - **High Volatility**: Whipsaws can cause losses
        - **Market Crashes**: Momentum can't predict sudden drops
        """)
    
    with tab3:
        st.markdown("""
        ## Risk Management Principles
        
        Making money is important, but **not losing money** is more important.
        
        ### Key Concepts
        
        #### 1. Position Sizing
        - Don't put all eggs in one basket
        - Typical: 5-20% per position
        - Our strategy: Equal-weight top stocks
        
        #### 2. Diversification
        - Spread risk across multiple stocks
        - Different sectors and industries
        - Consider global markets
        
        #### 3. Maximum Drawdown
        - Largest peak-to-trough decline
        - Example: If portfolio goes from $100k to $80k, drawdown = 20%
        - Important: Can you handle this psychologically?
        
        #### 4. Stop Losses
        - Automatic sell when price drops below threshold
        - Limits losses on individual positions
        - Our strategy: Rebalancing acts as dynamic stop
        
        ### The 1% Rule
        
        Never risk more than 1-2% of your portfolio on a single trade.
        
        Example:
        - Portfolio: $100,000
        - Max risk per trade: $1,000-$2,000
        - If stop loss is 10%, position size = $10,000-$20,000
        """)
    
    with tab4:
        st.markdown("""
        ## Key Performance Metrics
        
        ### 1. Total Return
        - Simple: (Ending Value - Starting Value) / Starting Value × 100%
        - Example: $100k → $120k = 20% return
        
        ### 2. Sharpe Ratio
        - Measures risk-adjusted returns
        - Formula: (Return - Risk-Free Rate) / Standard Deviation
        - **Good**: > 1.0, **Excellent**: > 2.0
        
        ### 3. Maximum Drawdown
        - Worst peak-to-trough decline
        - Shows worst-case scenario
        - Lower is better
        
        ### 4. Win Rate
        - Percentage of profitable trades
        - 50-60% is typical for momentum strategies
        - High win rate doesn't always mean profitable!
        
        ### 5. Profit Factor
        - Gross Profit / Gross Loss
        - Should be > 1.5 for good strategies
        - Example: $150k profit / $100k loss = 1.5
        
        ### 6. Volatility
        - Standard deviation of returns
        - Measures how much returns fluctuate
        - Higher volatility = higher risk
        """)

def show_momentum_strategy():
    """Interactive momentum strategy explanation"""
    st.header("🎯 Momentum Strategy Deep Dive")
    
    st.markdown("""
    This is the core strategy used in our backtests. Let's see it in action!
    """)
    
    # Interactive calculator
    st.subheader("📊 Momentum Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ticker = st.text_input("Enter Stock Ticker", value="AAPL", help="e.g., AAPL, MSFT, GOOGL")
        lookback = st.slider("Lookback Period (days)", 50, 300, 200)
    
    with col2:
        roc_period = st.slider("ROC Period (days)", 50, 300, 200)
        period = st.selectbox("Data Period", ["6mo", "1y", "2y", "5y"], index=1)
    
    if st.button("Calculate Momentum", type="primary"):
        with st.spinner(f"Fetching data for {ticker}..."):
            df = get_stock_data(ticker, period)
            
            if df is not None and len(df) > 0:
                # Calculate momentum
                momentum = calculate_momentum_score(df['Close'], lookback, roc_period)
                
                if momentum:
                    # Display results
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Momentum Score", f"{momentum['score']:.4f}")
                    with col2:
                        st.metric("ROC", f"{momentum['roc']:.2f}%")
                    with col3:
                        st.metric("Trend Slope", f"{momentum['slope']:.6f}")
                    with col4:
                        st.metric("Annualized Return", f"{momentum['annualized_return']:.2f}%")
                    
                    # Interpretation
                    if momentum['score'] > 0:
                        st.markdown(f"""
                        <div class="success-box">
                        <strong>✅ Positive Momentum</strong><br>
                        {ticker} shows upward momentum. The stock has been trending up with a {momentum['roc']:.2f}% 
                        rate of change over the past {roc_period} days.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="warning-box">
                        <strong>⚠️ Negative/Weak Momentum</strong><br>
                        {ticker} shows weak or negative momentum. Consider waiting for a stronger trend.
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Price chart
                    st.plotly_chart(plot_price_chart(df, ticker), use_container_width=True)
                    
                else:
                    st.error("Not enough data to calculate momentum. Try a longer period.")

def show_live_analysis():
    """Live market momentum analysis"""
    st.header("📊 Live Market Analysis")
    
    st.markdown("""
    Analyze momentum across popular stocks in real-time.
    """)
    
    # Predefined stock lists
    indices = {
        "Tech Giants": ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA"],
        "S&P 500 Top 10": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "BRK-B", "TSLA", "UNH", "JNJ"],
        "Dow Jones": ["AAPL", "MSFT", "JPM", "V", "UNH", "HD", "PG", "JNJ", "MA", "DIS"],
        "Custom": []
    }
    
    index_choice = st.selectbox("Select Stock List", list(indices.keys()))
    
    if index_choice == "Custom":
        custom_tickers = st.text_input("Enter tickers (comma-separated)", "AAPL,MSFT,GOOGL")
        tickers = [t.strip().upper() for t in custom_tickers.split(",")]
    else:
        tickers = indices[index_choice]
    
    lookback = st.slider("Lookback Period", 50, 300, 200, key="live_lookback")
    
    if st.button("Analyze Stocks", type="primary"):
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, ticker in enumerate(tickers):
            status_text.text(f"Analyzing {ticker}... ({i+1}/{len(tickers)})")
            progress_bar.progress((i + 1) / len(tickers))
            
            df = get_stock_data(ticker, "1y")
            if df is not None and len(df) > 0:
                momentum = calculate_momentum_score(df['Close'], lookback, lookback)
                if momentum:
                    results.append({
                        'Ticker': ticker,
                        'Momentum Score': momentum['score'],
                        'ROC %': momentum['roc'],
                        'Trend Slope': momentum['slope'],
                        'Ann. Return %': momentum['annualized_return'],
                        'Current Price': df['Close'].iloc[-1]
                    })
        
        status_text.empty()
        progress_bar.empty()
        
        if results:
            df_results = pd.DataFrame(results)
            df_results = df_results.sort_values('Momentum Score', ascending=False)
            
            st.subheader("🏆 Top Momentum Stocks")
            
            # Highlight top 3
            top_3 = df_results.head(3)
            cols = st.columns(3)
            for i, (idx, row) in enumerate(top_3.iterrows()):
                with cols[i]:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h2>#{i+1}</h2>
                        <h3>{row['Ticker']}</h3>
                        <p>Score: {row['Momentum Score']:.4f}</p>
                        <p>ROC: {row['ROC %']:.2f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.subheader("📋 Full Results")
            st.dataframe(df_results.style.background_gradient(subset=['Momentum Score'], cmap='RdYlGn'), use_container_width=True)
            
            # Visualization
            fig = px.bar(df_results, x='Ticker', y='Momentum Score', 
                        title='Momentum Scores Comparison',
                        color='Momentum Score',
                        color_continuous_scale='RdYlGn')
            st.plotly_chart(fig, use_container_width=True)

def show_backtest():
    """Simple backtest simulator"""
    st.header("🔬 Backtest Simulator")
    
    st.markdown("""
    Test the momentum strategy on historical data. See how it would have performed!
    """)
    
    st.info("🚧 Advanced backtesting with walk-forward optimization is available in the full system. This is a simplified version for learning.")
    
    ticker = st.text_input("Stock Ticker", "AAPL")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=730))
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    with col3:
        initial_capital = st.number_input("Initial Capital ($)", 10000, 1000000, 100000)
    
    if st.button("Run Backtest", type="primary"):
        with st.spinner("Running backtest..."):
            df = yf.download(ticker, start=start_date, end=end_date, progress=False)
            
            if df is not None and len(df) > 0:
                # Simple buy-and-hold comparison
                buy_hold_return = ((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100
                buy_hold_value = initial_capital * (1 + buy_hold_return / 100)
                
                st.subheader("📊 Results")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Buy & Hold Return", f"{buy_hold_return:.2f}%")
                    st.metric("Final Value", f"${buy_hold_value:,.2f}")
                with col2:
                    st.metric("Total Days", len(df))
                    st.metric("Start Price", f"${df['Close'].iloc[0]:.2f}")
                
                # Price chart
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name=ticker, line=dict(color='blue')))
                fig.update_layout(title=f'{ticker} Price History', yaxis_title='Price ($)', template='plotly_white')
                st.plotly_chart(fig, use_container_width=True)
                
                st.info("💡 For advanced momentum strategy backtesting with rebalancing, see the full Jupyter notebooks in the parent directory.")

def show_paper_trading():
    """Paper trading simulator"""
    st.header("🎮 Paper Trading Simulator")
    
    st.markdown("""
    Practice trading without risking real money!
    """)
    
    st.warning("🚧 Paper trading feature coming soon! This will allow you to simulate trades and track your virtual portfolio.")
    
    st.markdown("""
    ### What You'll Be Able To Do:
    
    - Start with virtual cash
    - Buy and sell stocks in real-time
    - Track your portfolio performance
    - Learn from mistakes without financial risk
    - Compare your performance to benchmarks
    
    ### Coming Features:
    
    - Real-time price updates
    - Order history and trade log
    - Performance analytics
    - Risk metrics
    - Leaderboard (compete with friends!)
    """)

def show_portfolio():
    """Portfolio tracking"""
    st.header("📈 Portfolio Tracker")
    
    st.markdown("""
    Track and analyze your investment portfolio.
    """)
    
    st.warning("🚧 Portfolio tracking feature coming soon!")
    
    st.markdown("""
    ### Planned Features:
    
    - Import your holdings
    - Real-time portfolio valuation
    - Performance tracking over time
    - Risk analysis and diversification metrics
    - Rebalancing recommendations
    - Tax loss harvesting opportunities
    """)

if __name__ == "__main__":
    main()


def show_advanced_strategies():
    """Advanced strategies from all Chotu projects"""
    st.header("🚀 Advanced Trading Strategies")
    
    st.markdown("""
    Explore professional trading strategies integrated from all Chotu projects:
    
    1. **Top-N Momentum TAA** - From Chotu-qstrader
    2. **60/40 Portfolio** - From Chotu-qstrader  
    3. **ROC × Trend Slope** - From root momentum files
    4. **Indicator-Based** - From Chotu-stock-analysis-engine
    """)
    
    if not ADVANCED_STRATEGIES_AVAILABLE:
        st.error("Advanced strategies module not available. Please check installation.")
        return
    
    # Strategy selection
    strategy_type = st.selectbox(
        "Select Strategy",
        [
            "Top-N Momentum TAA",
            "60/40 Portfolio",
            "ROC × Trend Slope",
            "Indicator-Based"
        ]
    )
    
    # Get strategy descriptions
    descriptions = get_strategy_descriptions()
    
    st.info(f"**{strategy_type}**: {descriptions.get(strategy_type, 'No description available')}")
    
    # Strategy-specific parameters
    if strategy_type == "Top-N Momentum TAA":
        col1, col2 = st.columns(2)
        with col1:
            lookback = st.slider("Momentum Lookback (days)", 60, 252, 126)
        with col2:
            top_n = st.slider("Number of Assets to Hold", 1, 10, 3)
        
        strategy = TopNMomentumStrategy(lookback=lookback, top_n=top_n)
        
    elif strategy_type == "60/40 Portfolio":
        col1, col2 = st.columns(2)
        with col1:
            stock_weight = st.slider("Stock Allocation %", 0, 100, 60) / 100
        with col2:
            bond_weight = 1 - stock_weight
            st.metric("Bond Allocation %", f"{bond_weight*100:.0f}%")
        
        strategy = SixtyFortyStrategy(stock_weight=stock_weight, bond_weight=bond_weight)
        
    elif strategy_type == "ROC × Trend Slope":
        col1, col2, col3 = st.columns(3)
        with col1:
            lookback = st.slider("Trend Lookback (days)", 50, 300, 200)
        with col2:
            roc_period = st.slider("ROC Period (days)", 50, 300, 200)
        with col3:
            top_n = st.slider("Top N Stocks", 1, 5, 1)
        
        strategy = ROCTrendMomentumStrategy(lookback=lookback, roc_period=roc_period, top_n=top_n)
        
    else:  # Indicator-Based
        col1, col2 = st.columns(2)
        with col1:
            min_buy = st.slider("Min Buy Indicators", 1, 3, 2)
        with col2:
            min_sell = st.slider("Min Sell Indicators", 1, 3, 2)
        
        strategy = IndicatorBasedStrategy(min_buy_indicators=min_buy, min_sell_indicators=min_sell)
    
    # Test the strategy
    st.subheader("📊 Test Strategy")
    
    # Stock selection
    if strategy_type == "60/40 Portfolio":
        st.info("Testing with SPY (stocks) and AGG (bonds)")
        tickers = ['SPY', 'AGG']
    else:
        ticker_input = st.text_input("Enter tickers (comma-separated)", "AAPL,MSFT,GOOGL,AMZN,NVDA")
        tickers = [t.strip().upper() for t in ticker_input.split(",")]
    
    period = st.selectbox("Data Period", ["6mo", "1y", "2y", "5y"], index=2)
    
    if st.button("Run Strategy Analysis", type="primary"):
        with st.spinner("Analyzing..."):
            # Fetch data
            prices_dict = {}
            for ticker in tickers:
                df = get_stock_data(ticker, period)
                if df is not None and len(df) > 0:
                    prices_dict[ticker] = df['Close']
            
            if len(prices_dict) == 0:
                st.error("No data available for the selected tickers.")
                return
            
            # Create DataFrame
            prices_df = pd.DataFrame(prices_dict)
            prices_df = prices_df.dropna()
            
            if len(prices_df) < 50:
                st.error("Not enough data for analysis.")
                return
            
            # Generate weights/signals
            if hasattr(strategy, 'generate_weights'):
                weights = strategy.generate_weights(prices_df)
                
                st.subheader("📋 Current Allocations")
                
                # Display weights
                weights_df = pd.DataFrame(list(weights.items()), columns=['Ticker', 'Weight'])
                weights_df = weights_df[weights_df['Weight'] > 0].sort_values('Weight', ascending=False)
                
                if len(weights_df) > 0:
                    st.dataframe(weights_df.style.format({'Weight': '{:.1%}'}), use_container_width=True)
                    
                    # Pie chart
                    fig = px.pie(weights_df, values='Weight', names='Ticker', 
                                title='Portfolio Allocation')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No positions recommended by strategy.")
                    
            elif hasattr(strategy, 'generate_signals'):
                # For indicator-based strategy
                st.subheader("📊 Signals for Each Stock")
                
                for ticker in tickers:
                    if ticker in prices_df.columns:
                        signals = strategy.generate_signals(prices_df[ticker])
                        
                        with st.expander(f"{ticker} - Action: {signals['action'].upper()}"):
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("RSI", f"{signals['rsi']:.1f}")
                            with col2:
                                st.metric("MACD", f"{signals['macd']:.2f}")
                            with col3:
                                st.metric("MA Cross", signals['ma_cross'])
                            
                            if signals['buy_signals']:
                                st.success(f"Buy Signals ({signals['num_buy']}): {', '.join(signals['buy_signals'])}")
                            if signals['sell_signals']:
                                st.error(f"Sell Signals ({signals['num_sell']}): {', '.join(signals['sell_signals'])}")

def show_strategy_comparison():
    """Compare multiple strategies"""
    st.header("⚔️ Strategy Comparison")
    
    st.markdown("""
    Compare all integrated strategies on the same data to see which performs best!
    
    This compares:
    - Top-N Momentum TAA (from Chotu-qstrader)
    - 60/40 Portfolio (from Chotu-qstrader)
    - ROC × Trend Slope (from root momentum files)
    - Indicator-Based (from Chotu-stock-analysis-engine)
    """)
    
    if not ADVANCED_STRATEGIES_AVAILABLE:
        st.error("Advanced strategies module not available.")
        return
    
    # Configuration
    col1, col2 = st.columns(2)
    
    with col1:
        ticker_input = st.text_input("Enter tickers (comma-separated)", "SPY,QQQ,IWM,AGG,TLT,GLD")
        tickers = [t.strip().upper() for t in ticker_input.split(",")]
    
    with col2:
        period = st.selectbox("Backtest Period", ["1y", "2y", "3y", "5y"], index=1)
        rebalance_freq = st.slider("Rebalance Frequency (days)", 7, 30, 21)
    
    if st.button("Compare All Strategies", type="primary"):
        with st.spinner("Running comparison..."):
            # Fetch data
            prices_dict = {}
            progress_bar = st.progress(0)
            
            for i, ticker in enumerate(tickers):
                progress_bar.progress((i + 1) / len(tickers))
                df = get_stock_data(ticker, period)
                if df is not None and len(df) > 0:
                    prices_dict[ticker] = df['Close']
            
            progress_bar.empty()
            
            if len(prices_dict) < 2:
                st.error("Need at least 2 tickers with data.")
                return
            
            # Create DataFrame
            prices_df = pd.DataFrame(prices_dict)
            prices_df = prices_df.dropna()
            
            if len(prices_df) < 200:
                st.warning("Limited data available. Results may not be reliable.")
            
            # Get all strategies
            strategies = get_all_strategies()
            
            # Run comparison
            comparison = StrategyComparison(strategies)
            results_df = comparison.backtest_all(prices_df, rebalance_freq=rebalance_freq)
            
            # Display results
            st.subheader("🏆 Strategy Performance Rankings")
            
            # Highlight top 3
            top_3 = results_df.head(3)
            cols = st.columns(3)
            
            for i, (idx, row) in enumerate(top_3.iterrows()):
                with cols[i]:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h2>#{i+1}</h2>
                        <h3>{row['Strategy']}</h3>
                        <p>Return: {row['Total Return %']:.2f}%</p>
                        <p>Final: ${row['Final Value']:,.0f}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Full results table
            st.subheader("📊 Complete Results")
            st.dataframe(
                results_df.style.format({
                    'Final Value': '${:,.2f}',
                    'Total Return %': '{:.2f}%'
                }).background_gradient(subset=['Total Return %'], cmap='RdYlGn'),
                use_container_width=True
            )
            
            # Bar chart
            fig = px.bar(
                results_df,
                x='Strategy',
                y='Total Return %',
                title='Strategy Performance Comparison',
                color='Total Return %',
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Analysis
            st.subheader("📈 Analysis")
            
            best_strategy = results_df.iloc[0]
            worst_strategy = results_df.iloc[-1]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.success(f"""
                **Best Performer**: {best_strategy['Strategy']}
                - Return: {best_strategy['Total Return %']:.2f}%
                - Final Value: ${best_strategy['Final Value']:,.2f}
                """)
            
            with col2:
                st.error(f"""
                **Worst Performer**: {worst_strategy['Strategy']}
                - Return: {worst_strategy['Total Return %']:.2f}%
                - Final Value: ${worst_strategy['Final Value']:,.2f}
                """)
            
            st.info(f"""
            **Performance Spread**: {best_strategy['Total Return %'] - worst_strategy['Total Return %']:.2f}%
            
            This shows how much strategy selection matters! The best strategy outperformed 
            the worst by {abs(best_strategy['Total Return %'] - worst_strategy['Total Return %']):.2f} percentage points.
            """)

