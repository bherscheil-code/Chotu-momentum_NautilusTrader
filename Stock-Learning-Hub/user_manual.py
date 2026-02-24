"""
User Manual Module - Interactive help system
"""
import streamlit as st

def show_user_manual():
    """Display comprehensive user manual"""
    st.markdown('<h1 class="main-header">📚 User Manual</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Welcome to Stock Learning Hub!
    
    This manual will guide you through every feature of the platform.
    """)
    
    # Quick navigation
    manual_section = st.selectbox(
        "Jump to section:",
        [
            "🚀 Quick Start Guide",
            "📖 Module Overview",
            "🎯 How to Use Each Module",
            "💡 Tips & Best Practices",
            "🔧 Troubleshooting",
            "❓ FAQ"
        ]
    )
    
    if manual_section == "🚀 Quick Start Guide":
        show_quick_start_guide()
    elif manual_section == "📖 Module Overview":
        show_module_overview()
    elif manual_section == "🎯 How to Use Each Module":
        show_module_usage()
    elif manual_section == "💡 Tips & Best Practices":
        show_tips()
    elif manual_section == "🔧 Troubleshooting":
        show_troubleshooting()
    elif manual_section == "❓ FAQ":
        show_faq()

def show_quick_start_guide():
    """Quick start guide"""
    st.header("🚀 Quick Start Guide")
    
    st.markdown("""
    ## Your First 5 Minutes
    
    ### Step 1: Learn the Basics (2 minutes)
    1. Click **"📖 Learn: Stock Basics"** in the left sidebar
    2. Read the **"Momentum Strategy"** tab
    3. Understand: **Momentum Score = ROC × Trend Slope**
    
    ### Step 2: Try the Calculator (2 minutes)
    1. Click **"🎯 Momentum Strategy"**
    2. Enter a stock ticker: `AAPL`
    3. Click **"Calculate Momentum"**
    4. See the results:
       - 🟢 Green box = Good momentum
       - 🟡 Yellow box = Weak momentum
    
    ### Step 3: Analyze Multiple Stocks (1 minute)
    1. Click **"📊 Live Market Analysis"**
    2. Select **"Tech Giants"**
    3. Click **"Analyze Stocks"**
    4. See which stocks have the strongest momentum
    
    ---
    
    ## What to Do Next
    
    ### Week 1: Basics
    - Read all tabs in "Learn: Stock Basics"
    - Calculate momentum for 10 different stocks
    - Compare Tech Giants, S&P 500 Top 10
    
    ### Week 2: Strategies
    - Go to "Advanced Strategies"
    - Try each of the 4 strategies
    - Adjust parameters and see results
    
    ### Week 3: Comparison
    - Use "Strategy Comparison"
    - Compare all strategies on same stocks
    - Understand which works best
    
    ### Week 4: Practice
    - Test strategies on different time periods
    - Analyze global markets
    - Build your investment intuition
    """)

def show_module_overview():
    """Overview of all modules"""
    st.header("📖 Module Overview")
    
    modules = {
        "🏠 Home": {
            "purpose": "Welcome screen and overview",
            "time": "2 minutes",
            "features": ["Feature highlights", "Learning path", "Getting started"]
        },
        "📖 Learn: Stock Basics": {
            "purpose": "Educational content about stocks and strategies",
            "time": "15 minutes",
            "features": ["What are stocks?", "Momentum strategy explained", "Risk management", "Key metrics"]
        },
        "🎯 Momentum Strategy": {
            "purpose": "Calculate momentum scores for individual stocks",
            "time": "5 minutes per stock",
            "features": ["Interactive calculator", "Real-time data", "Visual charts", "Score interpretation"]
        },
        "📊 Live Market Analysis": {
            "purpose": "Analyze multiple stocks simultaneously",
            "time": "5 minutes",
            "features": ["Batch analysis", "Predefined lists", "Custom tickers", "Visual comparison"]
        },
        "🔬 Backtest Simulator": {
            "purpose": "Test strategies on historical data",
            "time": "10 minutes",
            "features": ["Historical performance", "Buy-and-hold comparison", "Performance metrics"]
        },
        "🚀 Advanced Strategies": {
            "purpose": "Try 4 professional trading strategies",
            "time": "10 minutes per strategy",
            "features": ["Top-N Momentum", "60/40 Portfolio", "ROC × Trend Slope", "Indicator-Based"]
        },
        "⚔️ Strategy Comparison": {
            "purpose": "Compare all strategies side-by-side",
            "time": "5 minutes",
            "features": ["Performance rankings", "Visual charts", "Statistical analysis"]
        },
        "📚 User Manual": {
            "purpose": "This help system",
            "time": "As needed",
            "features": ["Quick start", "Module guides", "Tips", "Troubleshooting"]
        }
    }
    
    for module, info in modules.items():
        with st.expander(f"{module} - {info['purpose']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Time needed:** {info['time']}")
            with col2:
                st.markdown(f"**Features:** {len(info['features'])}")
            
            st.markdown("**What you can do:**")
            for feature in info['features']:
                st.markdown(f"- {feature}")

def show_module_usage():
    """Detailed usage instructions"""
    st.header("🎯 How to Use Each Module")
    
    module_choice = st.selectbox(
        "Select module for detailed instructions:",
        [
            "🎯 Momentum Strategy",
            "📊 Live Market Analysis",
            "🔬 Backtest Simulator",
            "🚀 Advanced Strategies",
            "⚔️ Strategy Comparison"
        ]
    )
    
    if module_choice == "🎯 Momentum Strategy":
        st.subheader("Momentum Strategy Calculator")
        st.markdown("""
        ### Purpose
        Calculate momentum scores for individual stocks to identify trending opportunities.
        
        ### Step-by-Step Instructions
        
        1. **Enter Stock Ticker**
           - Type the stock symbol (e.g., `AAPL`, `MSFT`, `GOOGL`)
           - Must be a valid ticker on Yahoo Finance
        
        2. **Adjust Parameters**
           - **Lookback Period**: Days for trend calculation (default: 200)
           - **ROC Period**: Days for rate of change (default: 200)
           - **Data Period**: How far back to fetch data (6mo, 1y, 2y, 5y)
        
        3. **Click "Calculate Momentum"**
           - App fetches real-time data
           - Calculates momentum score
           - Shows results
        
        4. **Interpret Results**
           - **Momentum Score**: Higher = stronger momentum
           - **ROC %**: Percentage change over period
           - **Trend Slope**: Direction and strength of trend
           - **Annualized Return**: Estimated yearly return
        
        5. **View Chart**
           - Candlestick price chart
           - 50-day and 200-day moving averages
           - Interactive zoom and pan
        
        ### Tips
        - Try different lookback periods to see sensitivity
        - Compare same stock across different time periods
        - Green box = positive momentum (consider buying)
        - Yellow box = weak/negative momentum (avoid)
        """)
    
    elif module_choice == "📊 Live Market Analysis":
        st.subheader("Live Market Analysis")
        st.markdown("""
        ### Purpose
        Analyze multiple stocks at once to find the best momentum opportunities.
        
        ### Step-by-Step Instructions
        
        1. **Select Stock List**
           - **Tech Giants**: AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA
           - **S&P 500 Top 10**: Largest US companies
           - **Dow Jones**: Industrial average components
           - **Custom**: Enter your own comma-separated list
        
        2. **Adjust Lookback Period**
           - Slider from 50 to 300 days
           - Default: 200 days (recommended)
        
        3. **Click "Analyze Stocks"**
           - Progress bar shows status
           - Fetches data for all stocks
           - Calculates momentum scores
        
        4. **Review Results**
           - **Top 3 Cards**: Highlighted winners
           - **Full Table**: All stocks with metrics
           - **Bar Chart**: Visual comparison
        
        5. **Sort and Filter**
           - Click column headers to sort
           - Find highest momentum scores
           - Compare across metrics
        
        ### Tips
        - Start with predefined lists to learn
        - Use custom lists for your watchlist
        - Higher momentum score = stronger trend
        - Compare ROC % to see recent performance
        """)
    
    elif module_choice == "🔬 Backtest Simulator":
        st.subheader("Backtest Simulator")
        st.markdown("""
        ### Purpose
        Test how strategies would have performed on historical data.
        
        ### Step-by-Step Instructions
        
        1. **Enter Stock Ticker**
           - Single stock to backtest
           - Example: `AAPL`, `SPY`, `QQQ`
        
        2. **Select Date Range**
           - **Start Date**: When to begin backtest
           - **End Date**: When to end backtest
           - Longer periods = more reliable results
        
        3. **Set Initial Capital**
           - How much money to start with
           - Default: $100,000
           - Range: $10,000 to $1,000,000
        
        4. **Click "Run Backtest"**
           - Calculates buy-and-hold performance
           - Shows final value
           - Displays metrics
        
        5. **Analyze Results**
           - **Total Return %**: Overall performance
           - **Final Value**: Ending portfolio value
           - **Price Chart**: Historical price movement
        
        ### Tips
        - Use at least 1 year of data
        - Compare to benchmark (SPY)
        - Understand past ≠ future
        - Test multiple time periods
        """)
    
    elif module_choice == "🚀 Advanced Strategies":
        st.subheader("Advanced Strategies")
        st.markdown("""
        ### Purpose
        Try 4 professional trading strategies with adjustable parameters.
        
        ### Available Strategies
        
        #### 1. Top-N Momentum TAA
        - Selects top N stocks by momentum
        - Equal-weight allocation
        - **Parameters**: Lookback period, Number of stocks
        
        #### 2. 60/40 Portfolio
        - Classic balanced portfolio
        - 60% stocks, 40% bonds
        - **Parameters**: Stock/Bond allocation
        
        #### 3. ROC × Trend Slope
        - Advanced momentum formula
        - Combines rate of change with trend
        - **Parameters**: Lookback, ROC period, Top N
        
        #### 4. Indicator-Based
        - Uses RSI, MACD, Moving Averages
        - Multiple signal confirmation
        - **Parameters**: Min buy/sell indicators
        
        ### Step-by-Step Instructions
        
        1. **Select Strategy**
           - Choose from dropdown
           - Read description
        
        2. **Adjust Parameters**
           - Use sliders to tune
           - See real-time updates
        
        3. **Enter Tickers**
           - Comma-separated list
           - Or use defaults
        
        4. **Click "Run Strategy Analysis"**
           - Fetches data
           - Applies strategy logic
           - Shows allocations
        
        5. **Review Results**
           - Current allocations
           - Pie chart visualization
           - Signal details (for indicator strategy)
        
        ### Tips
        - Start with default parameters
        - Adjust one parameter at a time
        - Compare results across strategies
        - Understand each strategy's logic
        """)
    
    elif module_choice == "⚔️ Strategy Comparison":
        st.subheader("Strategy Comparison")
        st.markdown("""
        ### Purpose
        Compare all 4 strategies on the same data to see which performs best.
        
        ### Step-by-Step Instructions
        
        1. **Enter Tickers**
           - Comma-separated list
           - Recommended: 6-10 stocks
           - Include mix of assets (stocks, bonds, commodities)
        
        2. **Select Backtest Period**
           - 1y, 2y, 3y, or 5y
           - Longer = more reliable
        
        3. **Set Rebalance Frequency**
           - Days between rebalances
           - Default: 21 days (monthly)
           - Range: 7-30 days
        
        4. **Click "Compare All Strategies"**
           - Runs all 4 strategies
           - Calculates performance
           - Ranks results
        
        5. **Analyze Results**
           - **Top 3 Cards**: Best performers
           - **Full Table**: All strategies ranked
           - **Bar Chart**: Visual comparison
           - **Analysis**: Performance spread
        
        ### Tips
        - Use diverse stock list
        - Test multiple time periods
        - Understand why some perform better
        - Consider risk vs return
        - No single strategy is always best
        """)

def show_tips():
    """Tips and best practices"""
    st.header("💡 Tips & Best Practices")
    
    st.markdown("""
    ## Learning Tips
    
    ### For Beginners
    1. **Start Slow**
       - Don't rush through modules
       - Understand each concept before moving on
       - Take notes on what you learn
    
    2. **Practice Regularly**
       - Use the app 2-3 times per week
       - Analyze different stocks each time
       - Build pattern recognition
    
    3. **Ask Questions**
       - Why does this stock have high momentum?
       - What makes strategies perform differently?
       - How do parameters affect results?
    
    ### For Analysis
    1. **Compare Multiple Stocks**
       - Don't analyze in isolation
       - Look for patterns across stocks
       - Understand relative strength
    
    2. **Use Different Time Periods**
       - Short-term (6mo): Recent trends
       - Medium-term (1-2y): Established patterns
       - Long-term (5y): Historical perspective
    
    3. **Adjust Parameters**
       - Try different lookback periods
       - See how results change
       - Understand sensitivity
    
    ## Strategy Tips
    
    ### Momentum Strategy
    - ✅ Works best in trending markets
    - ✅ Look for positive ROC AND positive slope
    - ❌ Avoid in choppy/sideways markets
    - ❌ Don't chase after big moves
    
    ### 60/40 Portfolio
    - ✅ Good for balanced risk/return
    - ✅ Rebalance monthly
    - ✅ Use SPY (stocks) and AGG (bonds)
    - ❌ May underperform in strong bull markets
    
    ### ROC × Trend Slope
    - ✅ Most sophisticated momentum approach
    - ✅ Combines multiple signals
    - ✅ Proven in backtests
    - ❌ Requires understanding of both components
    
    ### Indicator-Based
    - ✅ Multiple confirmation signals
    - ✅ Good for technical analysis
    - ✅ Clear buy/sell rules
    - ❌ Can give conflicting signals
    
    ## Risk Management
    
    ### Always Remember
    1. **Past Performance ≠ Future Results**
       - Historical data doesn't guarantee future success
       - Markets change constantly
       - Use as learning tool, not prediction
    
    2. **Diversification**
       - Don't put all money in one stock
       - Spread across multiple assets
       - Consider different sectors
    
    3. **Position Sizing**
       - Never risk more than 1-2% per trade
       - Start small when learning
       - Increase size as confidence grows
    
    4. **Stop Losses**
       - Know when to exit
       - Don't hold losing positions hoping for recovery
       - Protect your capital
    
    ## Common Mistakes to Avoid
    
    ### ❌ Don't Do This
    1. **Chasing Performance**
       - Don't buy just because stock went up
       - Look for sustainable momentum
       - Avoid FOMO (Fear of Missing Out)
    
    2. **Ignoring Risk**
       - Don't focus only on returns
       - Consider maximum drawdown
       - Understand volatility
    
    3. **Over-Trading**
       - Don't trade too frequently
       - Let strategies work
       - Be patient
    
    4. **Emotional Decisions**
       - Don't panic sell
       - Don't greed buy
       - Stick to your strategy
    
    ### ✅ Do This Instead
    1. **Follow Your Strategy**
       - Pick a strategy and stick to it
       - Give it time to work
       - Track results
    
    2. **Keep Learning**
       - Read about markets
       - Understand economics
       - Stay informed
    
    3. **Practice First**
       - Use this app extensively
       - Paper trade before real money
       - Build confidence
    
    4. **Start Small**
       - Begin with small amounts
       - Learn from mistakes
       - Scale up gradually
    """)

def show_troubleshooting():
    """Troubleshooting guide"""
    st.header("🔧 Troubleshooting")
    
    st.markdown("""
    ## Common Issues and Solutions
    
    ### App Won't Start
    
    **Problem**: Double-clicking run.bat does nothing
    
    **Solutions**:
    1. Check Python is installed:
       ```
       python --version
       ```
       Should show Python 3.9 or higher
    
    2. Install dependencies:
       ```
       pip install -r requirements.txt
       ```
    
    3. Run manually:
       ```
       streamlit run app.py
       ```
    
    ---
    
    ### Data Not Loading
    
    **Problem**: "Error fetching data" message
    
    **Solutions**:
    1. **Check Internet Connection**
       - App needs internet for stock data
       - Try opening a website
    
    2. **Verify Ticker Symbol**
       - Use correct format (AAPL, not Apple)
       - Check on Yahoo Finance first
    
    3. **Try Different Stock**
       - Some tickers may not have data
       - Use popular stocks (AAPL, MSFT, GOOGL)
    
    4. **Wait and Retry**
       - Yahoo Finance may be temporarily down
       - Try again in a few minutes
    
    ---
    
    ### Slow Performance
    
    **Problem**: App is slow or freezing
    
    **Solutions**:
    1. **Close Other Tabs**
       - Browser uses memory
       - Close unnecessary tabs
    
    2. **Restart App**
       - Stop with Ctrl+C
       - Run again
    
    3. **Use Shorter Periods**
       - Select 6mo or 1y instead of 5y
       - Reduces data to process
    
    4. **Analyze Fewer Stocks**
       - Start with 5-10 stocks
       - Not 50+ at once
    
    ---
    
    ### Calculation Errors
    
    **Problem**: "Not enough data" or "Cannot calculate"
    
    **Solutions**:
    1. **Use Longer Period**
       - Need at least 200 days for momentum
       - Select 1y or 2y period
    
    2. **Check Stock History**
       - New stocks may not have enough data
       - Use established companies
    
    3. **Adjust Parameters**
       - Reduce lookback period
       - Try 100-150 days instead of 200
    
    ---
    
    ### Charts Not Showing
    
    **Problem**: Blank space where chart should be
    
    **Solutions**:
    1. **Refresh Page**
       - Press F5 or reload
       - Charts should reappear
    
    2. **Check Browser**
       - Use Chrome, Firefox, or Edge
       - Update to latest version
    
    3. **Clear Cache**
       - Browser settings → Clear cache
       - Restart browser
    
    ---
    
    ### Strategy Comparison Fails
    
    **Problem**: "No results" or error in comparison
    
    **Solutions**:
    1. **Use More Stocks**
       - Need at least 3-4 stocks
       - Include mix of assets
    
    2. **Check Data Availability**
       - All stocks need data for period
       - Remove stocks with errors
    
    3. **Reduce Time Period**
       - Try 1y instead of 5y
       - Some stocks may not have long history
    
    ---
    
    ## Still Having Issues?
    
    ### Check These
    1. ✅ Python 3.9+ installed
    2. ✅ All dependencies installed
    3. ✅ Internet connection working
    4. ✅ Using valid stock tickers
    5. ✅ Browser is up to date
    
    ### Try This
    1. Restart the app
    2. Clear browser cache
    3. Try different stock
    4. Use shorter time period
    5. Check error message carefully
    """)

def show_faq():
    """Frequently asked questions"""
    st.header("❓ Frequently Asked Questions")
    
    faqs = {
        "General": [
            {
                "q": "Is this app free to use?",
                "a": "Yes! Completely free. No hidden costs, no subscriptions."
            },
            {
                "q": "Do I need to create an account?",
                "a": "No. The app runs locally on your computer. No registration needed."
            },
            {
                "q": "Can I use this for real trading?",
                "a": "This is an educational tool. Learn first, then consider real trading with proper research and risk management."
            },
            {
                "q": "Is my data safe?",
                "a": "Yes. Everything runs on your computer. No data is sent anywhere except to fetch stock prices from Yahoo Finance."
            }
        ],
        "Data & Analysis": [
            {
                "q": "Where does the stock data come from?",
                "a": "Yahoo Finance API. It's free and provides real-time data for most stocks."
            },
            {
                "q": "How often is data updated?",
                "a": "Data is fetched fresh each time you analyze. It's cached for 1 hour to improve performance."
            },
            {
                "q": "Can I analyze international stocks?",
                "a": "Yes! Use the correct ticker format (e.g., VOD.L for Vodafone London, BMW.DE for BMW Germany)."
            },
            {
                "q": "Why do some stocks show 'No data'?",
                "a": "Stock may be delisted, ticker may be wrong, or Yahoo Finance doesn't have data for it."
            }
        ],
        "Strategies": [
            {
                "q": "Which strategy is best?",
                "a": "No single strategy is always best. It depends on market conditions. Use Strategy Comparison to see which works for your stocks."
            },
            {
                "q": "Can I create my own strategy?",
                "a": "The code is open source! You can modify advanced_strategies.py to add your own."
            },
            {
                "q": "What's the difference between strategies?",
                "a": "Each uses different logic: Momentum TAA (holding period return), 60/40 (fixed allocation), ROC×Slope (advanced momentum), Indicator-Based (technical signals)."
            },
            {
                "q": "How do I know if a strategy is working?",
                "a": "Compare to buy-and-hold benchmark. Good strategy should outperform with acceptable risk."
            }
        ],
        "Technical": [
            {
                "q": "What is momentum?",
                "a": "Tendency of stocks that are rising to keep rising. We measure it with ROC (rate of change) and trend slope."
            },
            {
                "q": "What does ROC mean?",
                "a": "Rate of Change. Percentage change in price over a period. Formula: ((Current - Past) / Past) × 100"
            },
            {
                "q": "What is trend slope?",
                "a": "Direction and strength of price trend. Calculated using linear regression on log prices."
            },
            {
                "q": "What's a good momentum score?",
                "a": "Positive is good. Above 0.01 is strong. But compare across stocks - relative ranking matters more than absolute value."
            }
        ],
        "Learning": [
            {
                "q": "I'm a complete beginner. Where do I start?",
                "a": "Start with 'Learn: Stock Basics' module. Read all tabs. Then try Momentum Strategy with AAPL."
            },
            {
                "q": "How long to learn everything?",
                "a": "Basic understanding: 1 hour. Comfortable using all features: 1 week. Mastery: 1 month of regular practice."
            },
            {
                "q": "Should I paper trade before real trading?",
                "a": "Absolutely! Practice extensively with this app, then paper trade, then start small with real money."
            },
            {
                "q": "What books/resources do you recommend?",
                "a": "Start with: 'A Random Walk Down Wall Street' by Malkiel, 'The Intelligent Investor' by Graham. Then explore quantitative trading books."
            }
        ]
    }
    
    for category, questions in faqs.items():
        st.subheader(f"📌 {category}")
        for item in questions:
            with st.expander(f"**Q:** {item['q']}"):
                st.markdown(f"**A:** {item['a']}")
        st.markdown("---")
