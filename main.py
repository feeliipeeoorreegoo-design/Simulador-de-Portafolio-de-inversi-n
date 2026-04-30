import streamlit as st
from models.portfolio_model import Portfolio
from core.trading import buy, sell

if "portfolio" not in st.session_state:
    st.session_state.portfolio = None

st.title("Simulador de Portafolio")

if st.session_state.portfolio is None:
    capital = st.number_input("Capital inicial", value=10000)
    if st.button("Iniciar"):
        st.session_state.portfolio = Portfolio(capital)
        st.rerun()

portfolio = st.session_state.portfolio

if portfolio:
    asset = st.selectbox("Activo", ["AAPL", "TSLA", "MSFT"])
    amount = st.number_input("Monto")

    if st.button("Comprar"):
        msg = buy(portfolio, asset, amount)
        st.success(msg)

    shares = st.number_input("Acciones a vender")

    if st.button("Vender"):
        msg = sell(portfolio, asset, shares)
        st.success(msg)

    st.write("Cash:", portfolio.cash)
    st.write("Positions:", portfolio.positions)