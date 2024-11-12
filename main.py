import yfinance as yf
import pandas as pd
import streamlit as st
import altair as alt
import model
from prophet.plot import plot_plotly
from plotly import graph_objs as go
from prophet import Prophet

option = st.selectbox(
     'Which stock price would you like to see?',
     ('GOOGL', 'AAPL', 'MBG.DE','TSLA','ALV.DE','CNY'))

st.title(f" {option} Finance Stock Price App")

n_years = st.slider('Years of prediction:', 0, 4)
period = n_years * 365
tickerData = yf.Ticker(option)

tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2024-11-11')


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
random_forrest_model, X_test,Y_test = model.create_random_forrest_model(tickerdf=tickerData)

st.write(f" Random Forrest Model Score on test data: {random_forrest_model.score(X_test,Y_test)}")

last_data = tickerData[['SMA_20','SMA_50','RSI','Volume']].iloc[-1]
prediction = random_forrest_model.predict([last_data])
st.write(f'Current Price: ${tickerData["Close"].iloc[-1]:.2f}')
st.write(f'Predicted by RandomForrest Next Day Price: ${prediction[0]:.2f}')
        

#prophet
model_prophet, forecast = model.prophet_model(tickerData, period=period)

print(forecast.tail())
tomorrow_forecast = forecast.iloc[-1]

# Display results
st.write(f'Predicted by Prophet Next Day Price: ${tomorrow_forecast.yhat:.2f}')
st.write(f'Lower bound: ${tomorrow_forecast.yhat_lower:.2f}')
st.write(f'Upper bound: ${tomorrow_forecast.yhat_upper:.2f}')
st.write(f'Forecast plot for {n_years} years')

# Create plot using the model and forecast
fig = plot_plotly(model_prophet, forecast)  # Pass both model and forecast
st.plotly_chart(fig)