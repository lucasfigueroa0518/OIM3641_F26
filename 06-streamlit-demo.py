from datetime import date, timedelta
import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

END = date.today()
START = date.today () - timedelta(days=365)

st.title("Stock Analysis")

st. set_page_config(layout="wide",
                    page_title="Stock Price Analysis")
st.title("Stock Price Analysis")

st.sidebar.title("Inputs")
ticker = st.sidebar.text_input("Enter stock ticker symbol")
col1, col2 = st.sidebar.columns(2)
start_date = st.sidebar.date_input("Start Date", START)
end_date = col2.date_input("End_Date", END)
st.sidebar.slider("Moving Average",
                  min_value = 0,
                  max_value= 100,
                  value = 10)
run_analysis = st.sidebar.button("Run Analysis", type="primary")

def get_stock_date(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start_date, end_date)
        if data.empty:
            return None, f"No data for {ticker}"
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        return data, f"Successfully downloaded data {ticker}"
    except Exception as e:
            return None, f"Donload failed due to {e}"





