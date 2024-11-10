import yfinance as yf
import pandas as pd
import streamlit as st
import altair as alt


option = st.selectbox(
     'Which stock price would you like to see?',
     ('GOOGL', 'AAPL', 'MBG.DE'))

st.title(f" {option} Finance Stock Price App")


tickerData = yf.Ticker(option)

tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')


# Create a line chart for the Close prices
close_chart = alt.Chart(tickerDf.reset_index()).mark_line(color='green').encode(
    x='Date:T',
    y='Close:Q'
)

# Create a line chart for the Volume
volume_chart = alt.Chart(tickerDf.reset_index()).mark_line(color='orange').encode(
    x='Date:T',
    y='Volume:Q'
)
st.title('Closing Price')
st.altair_chart(close_chart, use_container_width=True)

st.title('Volume')
st.altair_chart(volume_chart, use_container_width=True)