#!/bin/bash

echo "========================================"
echo "Stock Learning Hub - Linux/Mac Launcher"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9+ from https://www.python.org/"
    exit 1
fi

echo "[1/3] Checking virtual environment..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "[2/3] Activating virtual environment..."
source venv/bin/activate

echo "[3/3] Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "========================================"
echo "Starting Stock Learning Hub..."
echo "========================================"
echo ""
echo "Open your browser to: http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py
