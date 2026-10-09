from datetime import date, timedelta

import numpy as np
import plotly.express as px
import streamlit as st
import yfinance as yf

START = date.today() - timedelta(days=365)
END = date.today()

st.set_page_config(layout="wide", page_title="Stock Price Analysis")
st.title("Stock Analysis")

st.sidebar.title("Inputs")
ticker = st.sidebar.text_input("Ticker symbol", placeholder="AAPL")
start_date = st.sidebar.date_input("Start date", value=START)
end_date = st.sidebar.date_input("End date", value=END)
ma_window = st.sidebar.slider(
    "Moving Average Window",
    min_value=5,
    max_value=200,
    value=10,
)
ma_window_2 = st.sidebar.slider(
    "Second moving average window",
    min_value=5,
    max_value=200,
    value=50,
)
run_analysis = st.sidebar.button("Run Analysis", type="primary")


def download_prices(symbol, start, end):
    try:
        data = yf.download(
            symbol,
            start=start,
            end=end,
            progress=False,
            multi_level_index=False,
        )
        if data.empty:
            return None, f"No data for {symbol}"
        return data, f"Successfully downloaded for {symbol}"
    except Exception as e:
        return None, f"Failed due to {e}"


if run_analysis:
    symbol = ticker.strip().upper()
    if symbol == "":
        st.session_state["prices"] = None
        st.session_state["message"] = "Enter a ticker symbol."
    else:
        with st.spinner(f"Downloading {symbol}..."):
            prices, message = download_prices(symbol, start_date, end_date)
        st.session_state["prices"] = prices
        st.session_state["message"] = message
        st.session_state["symbol"] = symbol

prices = st.session_state.get("prices")
message = st.session_state.get("message")

if prices is None:
    if message:
        st.error(message)
    else:
        st.info("Enter a ticker and click Run Analysis.")
else:
    st.success(message)
    prices = prices.copy()
    prices["change"] = prices["Close"] - prices["Close"].shift(1)
    prices["return"] = np.log(prices["Close"]).diff().round(4)
    prices = prices.dropna()
    prices["MA"] = prices["Close"].rolling(window=ma_window).mean()
    prices["MA2"] = prices["Close"].rolling(window=ma_window_2).mean()

    last_close = prices["Close"].iloc[-1]
    cumulative_return = prices["return"].sum()
    trading_days = len(prices)
    col1, col2, col3 = st.columns(3)
    col1.metric("Last close", f"${last_close:,.2f}")
    col2.metric("Cumulative return", f"{cumulative_return:.2%}")
    col3.metric("Trading days", trading_days)

    price_fig = px.line(
        prices,
        y=["Close", "MA", "MA2"],
        title=f"{st.session_state['symbol']} close, {ma_window}-day and {ma_window_2}-day moving averages",
    )
    price_fig.update_layout(yaxis_title="Price", hovermode="x unified")
    st.plotly_chart(price_fig, width="stretch")
