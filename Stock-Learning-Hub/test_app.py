"""
Test script for Stock Learning Hub
Run this to verify everything is working correctly
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Test that all required packages can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit
        print("✓ streamlit")
    except ImportError as e:
        print(f"✗ streamlit: {e}")
        return False
    
    try:
        import pandas
        print("✓ pandas")
    except ImportError as e:
        print(f"✗ pandas: {e}")
        return False
    
    try:
        import numpy
        print("✓ numpy")
    except ImportError as e:
        print(f"✗ numpy: {e}")
        return False
    
    try:
        import yfinance
        print("✓ yfinance")
    except ImportError as e:
        print(f"✗ yfinance: {e}")
        return False
    
    try:
        import plotly
        print("✓ plotly")
    except ImportError as e:
        print(f"✗ plotly: {e}")
        return False
    
    return True

def test_utils():
    """Test utility functions"""
    print("\nTesting utility functions...")
    
    try:
        from utils import calculate_momentum_score
        import pandas as pd
        import numpy as np
        
        # Create sample data
        prices = pd.Series(np.random.randn(300).cumsum() + 100)
        
        # Test momentum calculation
        result = calculate_momentum_score(prices, lookback=200, roc_period=200)
        
        if result is not None:
            print("✓ calculate_momentum_score")
            print(f"  Sample score: {result['score']:.4f}")
        else:
            print("✗ calculate_momentum_score returned None")
            return False
            
    except Exception as e:
        print(f"✗ calculate_momentum_score: {e}")
        return False
    
    return True

def test_data_fetch():
    """Test data fetching"""
    print("\nTesting data fetching...")
    
    try:
        import yfinance as yf
        
        # Try to fetch data for a popular stock
        ticker = "AAPL"
        stock = yf.Ticker(ticker)
        df = stock.history(period="1mo")
        
        if len(df) > 0:
            print(f"✓ Data fetch successful for {ticker}")
            print(f"  Fetched {len(df)} days of data")
        else:
            print(f"✗ No data returned for {ticker}")
            return False
            
    except Exception as e:
        print(f"✗ Data fetch failed: {e}")
        return False
    
    return True

def test_calculations():
    """Test momentum calculations with real data"""
    print("\nTesting calculations with real data...")
    
    try:
        import yfinance as yf
        from utils import calculate_momentum_score
        
        # Fetch real data
        ticker = "AAPL"
        stock = yf.Ticker(ticker)
        df = stock.history(period="1y")
        
        if len(df) < 200:
            print(f"⚠ Not enough data for {ticker} (need 200+ days)")
            return True  # Not a failure, just insufficient data
        
        # Calculate momentum
        result = calculate_momentum_score(df['Close'], lookback=200, roc_period=200)
        
        if result is not None:
            print(f"✓ Momentum calculation successful for {ticker}")
            print(f"  Momentum Score: {result['score']:.4f}")
            print(f"  ROC: {result['roc']:.2f}%")
            print(f"  Trend Slope: {result['slope']:.6f}")
            print(f"  Annualized Return: {result['annualized_return']:.2f}%")
        else:
            print(f"✗ Momentum calculation returned None for {ticker}")
            return False
            
    except Exception as e:
        print(f"✗ Calculation failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("Stock Learning Hub - Test Suite")
    print("=" * 60)
    
    all_passed = True
    
    # Run tests
    if not test_imports():
        all_passed = False
        print("\n⚠ Import test failed. Run: pip install -r requirements.txt")
    
    if not test_utils():
        all_passed = False
        print("\n⚠ Utils test failed.")
    
    if not test_data_fetch():
        all_passed = False
        print("\n⚠ Data fetch test failed. Check internet connection.")
    
    if not test_calculations():
        all_passed = False
        print("\n⚠ Calculation test failed.")
    
    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed!")
        print("\nYou can now run the app:")
        print("  streamlit run app.py")
    else:
        print("✗ Some tests failed.")
        print("\nPlease fix the issues above before running the app.")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
