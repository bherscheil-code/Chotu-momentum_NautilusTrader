"""
Technical Analysis Module for Streamlit App
Complete integration from Chotu-stock-analysis-engine
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def show_technical_analysis():
    """
    Comprehensive Technical Analysis Module
    100% integration from Chotu-stock-analysis-engine
    """
    st.header("📈 Technical Analysis - Complete Suite")
    
    st.markdown("""
    **Professional technical analysis with 12+ indicators!**
    
    From Chotu-stock-analysis-engine - Now fully integrated:
    - RSI, MACD, Bollinger Bands
    - Stochastic, Williams %R
    - OBV, ROC, ATR, ADX
    - CCI, MFI
    - Multi-indicator signals
    """)
    
    if not TECHNICAL_INDICATORS_AVAILABLE:
        st.error("Technical indicators module not available.")
        return
    
    # Stock selection
    col1, col2 = st.columns(2)
    
    with col1:
        ticker = st.text_input("Enter Stock Ticker", value="AAPL", help="e.g., AAPL, MSFT, GOOGL")
    
    with col2:
        period = st.selectbox("Data Period", ["6mo", "1y", "2y", "5y"], index=1)
    
    # Analysis parameters
    st.subheader("⚙️ Analysis Settings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_buy = st.slider("Min Buy Indicators", 1, 5, 3, help="Minimum indicators saying buy to trigger")
    
    with col2:
        min_sell = st.slider("Min Sell Indicators", 1, 5, 3, help="Minimum indicators saying sell to trigger")
    
    with col3:
        show_all_indicators = st.checkbox("Show All Indicators", value=True)
    
    if st.button("Run Technical Analysis", type="primary"):
        with st.spinner(f"Analyzing {ticker}..."):
            # Fetch data
            df = get_stock_data(ticker, period)
            
            if df is None or len(df) < 50:
                st.error("Not enough data. Need at least 50 days of history.")
                return
            
            # Run analysis
            analyzer = AdvancedTechnicalAnalysis(min_buy_indicators=min_buy, min_sell_indicators=min_sell)
            results = analyzer.analyze_stock(df)
            
            if 'error' in results:
                st.error(results['error'])
                return
            
            # Display action
            st.subheader("🎯 Trading Signal")
            
            action = results['action'].upper()
            if action == 'BUY':
                st.success(f"**{action}** - {results['num_buy']} indicators saying BUY")
            elif action == 'SELL':
                st.error(f"**{action}** - {results['num_sell']} indicators saying SELL")
            else:
                st.info(f"**{action}** - Mixed signals")
            
            # Display signals
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Buy Signals", results['num_buy'])
                if results['buy_signals']:
                    st.success("**Buy Indicators:**")
                    for signal in results['buy_signals']:
                        st.write(f"✅ {signal}")
            
            with col2:
                st.metric("Sell Signals", results['num_sell'])
                if results['sell_signals']:
                    st.error("**Sell Indicators:**")
                    for signal in results['sell_signals']:
                        st.write(f"❌ {signal}")
            
            with col3:
                st.metric("Trend Strength", results['trend_strength'].upper())
                st.metric("Current Price", f"${results['indicators']['price']:.2f}")
            
            # Key indicators
            st.subheader("📊 Key Indicators")
            
            indicators = results['indicators']
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                rsi_color = "🟢" if indicators['rsi'] < 30 else ("🔴" if indicators['rsi'] > 70 else "🟡")
                st.metric(f"{rsi_color} RSI", f"{indicators['rsi']:.1f}")
                st.caption("< 30: Oversold, > 70: Overbought")
            
            with col2:
                macd_color = "🟢" if indicators['macd'] > indicators['macd_signal'] else "🔴"
                st.metric(f"{macd_color} MACD", f"{indicators['macd']:.2f}")
                st.caption(f"Signal: {indicators['macd_signal']:.2f}")
            
            with col3:
                stoch_color = "🟢" if indicators['stoch_k'] < 20 else ("🔴" if indicators['stoch_k'] > 80 else "🟡")
                st.metric(f"{stoch_color} Stochastic", f"{indicators['stoch_k']:.1f}")
                st.caption("< 20: Oversold, > 80: Overbought")
            
            with col4:
                adx_color = "🟢" if indicators['adx'] > 25 else "🟡"
                st.metric(f"{adx_color} ADX", f"{indicators['adx']:.1f}")
                st.caption("> 25: Strong trend")
            
            # All indicators table
            if show_all_indicators:
                st.subheader("📋 All Indicators")
                
                indicators_df = pd.DataFrame([
                    {"Indicator": "RSI", "Value": f"{indicators['rsi']:.2f}", "Signal": "Oversold" if indicators['rsi'] < 30 else ("Overbought" if indicators['rsi'] > 70 else "Neutral")},
                    {"Indicator": "MACD", "Value": f"{indicators['macd']:.2f}", "Signal": "Bullish" if indicators['macd'] > indicators['macd_signal'] else "Bearish"},
                    {"Indicator": "Stochastic %K", "Value": f"{indicators['stoch_k']:.2f}", "Signal": "Oversold" if indicators['stoch_k'] < 20 else ("Overbought" if indicators['stoch_k'] > 80 else "Neutral")},
                    {"Indicator": "Williams %R", "Value": f"{indicators['williams_r']:.2f}", "Signal": "Oversold" if indicators['williams_r'] < -80 else ("Overbought" if indicators['williams_r'] > -20 else "Neutral")},
                    {"Indicator": "ROC", "Value": f"{indicators['roc']:.2f}%", "Signal": "Positive" if indicators['roc'] > 0 else "Negative"},
                    {"Indicator": "ADX", "Value": f"{indicators['adx']:.2f}", "Signal": "Strong Trend" if indicators['adx'] > 25 else "Weak Trend"},
                    {"Indicator": "CCI", "Value": f"{indicators['cci']:.2f}", "Signal": "Oversold" if indicators['cci'] < -100 else ("Overbought" if indicators['cci'] > 100 else "Neutral")},
                    {"Indicator": "MFI", "Value": f"{indicators['mfi']:.2f}", "Signal": "Oversold" if indicators['mfi'] < 20 else ("Overbought" if indicators['mfi'] > 80 else "Neutral")},
                    {"Indicator": "ATR", "Value": f"{indicators['atr']:.2f}", "Signal": "High Volatility" if indicators['atr'] > df['Close'].iloc[-1] * 0.02 else "Low Volatility"},
                ])
                
                st.dataframe(indicators_df, use_container_width=True)
            
            # Charts
            st.subheader("📈 Technical Charts")
            
            # Create subplots
            fig = make_subplots(
                rows=4, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.05,
                subplot_titles=('Price & Bollinger Bands', 'RSI', 'MACD', 'Stochastic'),
                row_heights=[0.4, 0.2, 0.2, 0.2]
            )
            
            # Price and Bollinger Bands
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name='Price'
            ), row=1, col=1)
            
            fig.add_trace(go.Scatter(
                x=df.index,
                y=results['series']['bb_upper'],
                name='BB Upper',
                line=dict(color='gray', dash='dash')
            ), row=1, col=1)
            
            fig.add_trace(go.Scatter(
                x=df.index,
                y=results['series']['bb_middle'],
                name='BB Middle',
                line=dict(color='blue')
            ), row=1, col=1)
            
            fig.add_trace(go.Scatter(
                x=df.index,
                y=results['series']['bb_lower'],
                name='BB Lower',
                line=dict(color='gray', dash='dash')
            ), row=1, col=1)
            
            # RSI
            fig.add_trace(go.Scatter(
                x=df.index,
                y=results['series']['rsi'],
                name='RSI',
                line=dict(color='purple')
            ), row=2, col=1)
            
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
            
            # MACD
            fig.add_trace(go.Scatter(
                x=df.index,
                y=results['series']['macd'],
                name='MACD',
                line=dict(color='blue')
            ), row=3, col=1)
            
            fig.add_trace(go.Scatter(
                x=df.index,
                y=results['series']['macd_signal'],
                name='Signal',
                line=dict(color='red')
            ), row=3, col=1)
            
            # Stochastic
            fig.add_trace(go.Scatter(
                x=df.index,
                y=results['series']['stoch_k'],
                name='%K',
                line=dict(color='blue')
            ), row=4, col=1)
            
            fig.add_trace(go.Scatter(
                x=df.index,
                y=results['series']['stoch_d'],
                name='%D',
                line=dict(color='red')
            ), row=4, col=1)
            
            fig.add_hline(y=80, line_dash="dash", line_color="red", row=4, col=1)
            fig.add_hline(y=20, line_dash="dash", line_color="green", row=4, col=1)
            
            fig.update_layout(
                height=1200,
                showlegend=True,
                template='plotly_white'
            )
            
            fig.update_xaxes(rangeslider_visible=False)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Interpretation
            st.subheader("💡 Interpretation")
            
            st.markdown(f"""
            ### Current Analysis for {ticker}
            
            **Action:** {action}
            
            **Why?**
            - {results['num_buy']} indicators are saying BUY
            - {results['num_sell']} indicators are saying SELL
            - Trend strength is {results['trend_strength']}
            
            **Buy Signals:** {', '.join(results['buy_signals']) if results['buy_signals'] else 'None'}
            
            **Sell Signals:** {', '.join(results['sell_signals']) if results['sell_signals'] else 'None'}
            
            **Remember:**
            - This is technical analysis only
            - Consider fundamentals too
            - Use proper risk management
            - Past performance ≠ future results
            """)
