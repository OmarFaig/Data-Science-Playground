import yfinance as yf
import pandas as pd
import streamlit as st
import altair as alt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime,timedelta
from prophet import Prophet
#download the data for the given timeframe

@st.cache_data
def download_data(stocks):
    tickerData = yf.Ticker(stocks)
    tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2022-11-11')
    return tickerDf


def calculate_relative_strength(prices, period=14):
    """
    Calculates the Relative Strength Index (RSI) for a given set of stock prices.

    The Relative Strength Index (RSI) is a momentum indicator that measures speed/magnitude of price changes.
    It ranges from 0 to 100. A value above 70 indicates an overbought condition, while a value below 30 indicates an oversold condition.

    Parameters:
    prices (pandas.Series): A pandas Series containing the historical stock prices.
    period (int, optional): The number of days to consider for the calculation. Default is 14.

    Returns:
    pandas.Series: A pandas Series containing the calculated RSI values.
    """
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

     
def prepare_data(tickerdf):
     """
     This function prepares the given ticker data by calculating the Simple Moving Average (SMA) for 20 and 50 days,
     and the Relative Strength Index (RSI). The function also drops any NaN values resulting from the calculations.
 
     Parameters:
     tickerdf (pandas.DataFrame): A DataFrame containing the historical stock prices. The DataFrame should have a 'Close' column.
 
     Returns:
     pandas.DataFrame: The prepared DataFrame with additional columns for SMA_20, SMA_50, and RSI.
     """
     # 20-days closing price mean - SMA20 - Simple Moving Average
     tickerdf['SMA_20'] = tickerdf['Close'].rolling(window=20).mean()
     tickerdf['SMA_50'] = tickerdf['Close'].rolling(window=50).mean()
 
     # Relative strength index - RSI 
     # Momentum indicator that measures speed/magnitude of price changes
     # Values range 0-100
     # Above 70 = overbought, Below 30 = oversold
     tickerdf['RSI'] = calculate_relative_strength(tickerdf['Close'])
 
     # Drop any NaN values resulting from the calculations
     tickerdf = tickerdf.dropna()
 
     return tickerdf

def create_random_forrest_model(tickerdf):

    X = tickerdf[['SMA_20', 'SMA_50', 'RSI','Volume']]
    y = tickerdf['Close'].shift(-1) # prediction of next day's closing price
    #remove last row since it is nan in y
    X = X[:-1]
    y = y[:-1]

    #split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Create and train the Random Forest Regressor model
    model = RandomForestRegressor(n_estimators=100,random_state=42)
    model.fit(X_train, y_train)
    return model, X_test, y_test

    

#TEST ABOVE FUNCTION
#TEST ABOVE FUNCTION
#option = 'AAPL'
#data = download_data(option)
#print(data.head())
#data = prepare_data(data)
#print(data.head())
#print(create_model(data))

#using prophet
def prophet_model(data,period=None):
    # Reset index and make copy to avoid modifying original data
    data = data.reset_index()
    
    # Convert timezone-aware dates to timezone-naive
    data['Date'] = data['Date'].dt.tz_localize(None)
    
    df_train = data[['Date','Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

        # Initialize and fit model
    model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=True
        )
        
    model.fit(df_train)
    
    # Create future dates
    if period is None:
        period = 365  # Default to 1 year
    future = model.make_future_dataframe(periods=period)
    
    # Make prediction
    forecast = model.predict(future)
    
    return model, forecast
        
