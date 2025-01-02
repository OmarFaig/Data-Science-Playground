# Stock Price Prediction App

A machine learning application that predicts stock prices using Random Forest and Facebook Prophet models. Built with Python, Streamlit, and yfinance.

## Features

- Real-time stock data fetching using yfinance
- Technical indicators calculation (SMA, RSI)
- Two prediction models:
  - Random Forest (short-term predictions)
  - Facebook Prophet (long-term forecasting)
- Interactive web interface using Streamlit
- Visual analytics with Plotly and Altair

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stock-prediction-app.git
cd stock-prediction-app
python -m venv stockvenv
source stockvenv/bin/activate  # Linux/Mac