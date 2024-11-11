import yfinance as yf
import pandas as pd
import streamlit as st
import altair as alt
import model

option = st.selectbox(
     'Which stock price would you like to see?',
     ('GOOGL', 'AAPL', 'MBG.DE','TSLA','ALV.DE','CNY'))

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
tickerData = model.prepare_data(tickerdf=tickerDf)
model, X_test,Y_test = model.create_model(tickerdf=tickerData)

st.write(f"Model Score on test data: {model.score(X_test,Y_test)}")

last_data = tickerData[['SMA_20','SMA_50','RSI','Volume']].iloc[-1]
prediction = model.predict([last_data])
st.write(f'Current Price: ${tickerData["Close"].iloc[-1]:.2f}')
st.write(f'Predicted Next Day Price: ${prediction[0]:.2f}')
        

