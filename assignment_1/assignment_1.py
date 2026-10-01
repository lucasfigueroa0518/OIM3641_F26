import streamlit as st

from stock import Stock

st.set_page_config(layout="wide", page_title="Stock Price Analysis")
st.title("Stock Analysis")

single_tab, portfolio_tab = st.tabs(
    ["Single Stock Analysis", "Portfolio Comparison"]
)
