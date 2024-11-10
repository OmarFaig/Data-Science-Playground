import yfinance as yf
import pandas as pd
import streamlit as st
import altair as alt

#download the data for the given timeframe
def download_data(option):
    tickerData = yf.Ticker(option)
    tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')
    return tickerDf

#TEST ABOVE FUNCTION
#option = 'AAPL'
#data = download_data(option)
#print(data.head())
