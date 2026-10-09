
import pandas as pd
import plotly.express as px
import streamlit as st

from stock import Stock
from datetime import date, timedelta
START = date.today() - timedelta(days=365)
END = date.today()

st.set_page_config(layout="wide", page_title="Stock Price Analysis")


@st.cache_data
def load_stock(symbol, start, end, ma_window):
    return Stock(symbol, start, end, ma_window)


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

if run_analysis:
    symbol = ticker.strip().upper()
    if symbol == "":
        st.session_state["stock"] = None
    else:
        with st.spinner(f"Downloading {symbol}..."):
            st.session_state["stock"] = load_stock(
                symbol, start_date, end_date, ma_window
            )

single_tab, portfolio_tab = st.tabs(
    ["Single Stock Analysis", "Portfolio Comparison"]
)

with single_tab:
    stock = st.session_state.get("stock")
    if stock is None:
        st.info("Enter a ticker and click Run Analysis.")
    elif stock.data is None:
        st.error(stock.message)
    else:
        st.success(stock.message)
        last_close = stock.data["Close"].iloc[-1]
        cumulative_return = stock.data["return"].sum()
        trading_days = len(stock.data)
        col1, col2, col3 = st.columns(3)
        col1.metric("Last close", f"${last_close:,.2f}")
        col2.metric("Cumulative return", f"{cumulative_return:.2%}")
        col3.metric("Trading days", trading_days)

        price = stock.data.copy()
        price[f"{ma_window_2}-day MA"] = price["Close"].rolling(window=ma_window_2).mean()
        price_fig = px.line(
            price,
            y=["Close", "MA", f"{ma_window_2}-day MA"],
            title=(
                f"{stock.symbol} close, {stock.ma_window}-day and "
                f"{ma_window_2}-day moving averages"
            ),
        )
        price_fig.update_layout(yaxis_title="Price", hovermode="x unified")
        st.plotly_chart(price_fig, width="stretch")
        st.plotly_chart(stock.plot_performance(), width="stretch")
        st.plotly_chart(stock.plot_return_dist(), width="stretch")
        st.dataframe(stock.data["return"].describe())

with portfolio_tab:
    portfolio_input = st.text_input(
        "Tickers, separated by commas",
        placeholder="AAPL, MSFT, GOOG",
    )
    if run_analysis:
        tickers = [
            symbol.strip().upper()
            for symbol in portfolio_input.split(",")
            if symbol.strip()
        ]
        series = {}
        errors = []
        if tickers:
            with st.spinner("Downloading portfolio..."):
                for symbol in tickers:
                    holding = load_stock(symbol, start_date, end_date, ma_window)
                    if holding.data is None:
                        errors.append(holding.message)
                        continue
                    cumulative = holding.data["return"].cumsum()
                    series[symbol] = cumulative - cumulative.iloc[0]
        st.session_state["portfolio"] = pd.DataFrame(series)
        st.session_state["portfolio_errors"] = errors

    for message in st.session_state.get("portfolio_errors", []):
        st.error(message)

    portfolio = st.session_state.get("portfolio")
    if portfolio is not None and not portfolio.empty:
        portfolio_fig = px.line(
            portfolio,
            title="Zero-based cumulative performance",
        )
        portfolio_fig.update_layout(
            yaxis_title="Cumulative return",
            yaxis_tickformat=".1%",
            hovermode="x unified",
            legend_title_text="Ticker",
        )
        portfolio_fig.add_hline(y=0, line_dash="dash", line_color="black", opacity=0.7)
        st.plotly_chart(portfolio_fig, width="stretch")
    elif not st.session_state.get("portfolio_errors"):
        st.info("Enter tickers and click Run Analysis.")


