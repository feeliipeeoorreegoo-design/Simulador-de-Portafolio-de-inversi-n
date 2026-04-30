"""
Simulador Interactivo de Portafolio con Streamlit

Ejecutar:
    streamlit run app.py

Requisitos:
    pip install streamlit pandas numpy matplotlib
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import timedelta

# -----------------------------
# CONFIGURACIÓN INICIAL
# -----------------------------
st.set_page_config(page_title="Simulador de Portafolio de Inversiones", layout="wide")

st.title("📈 Simulador Interactivo de Portafolio")

# -----------------------------
# ESTADO GLOBAL (persistencia)
# -----------------------------

if "portfolio" not in st.session_state:
    st.session_state.portfolio = {
        "cash": 0,
        "positions": {},
        "history": []
    }

# Comisiones por acción

COMISIONES = {
    "APPLE": 0.002, # Apple
    "TESLA": 0.0015, # Tesla
    "MICROSOFT": 0.002, # Microsoft
    "AMAZON": 0.002, # Amazon
    "GOOGLE": 0.0012, # Google
    "JPMORGAN": 0.0018, # JP Morgan Chase & Co.
    "JOHNSON_AND_JOHNSON": 0.0016, #Johnson & Johnson
    "VISA": 0.0015, #Visa INC
    "PROCTER_AND_GAMBLE": 0.0021, # Procter & Gramble
    "DISNEY": 0.0010 # The Walt Disney Company
}

# -----------------------------
# INPUT CAPITAL INICIAL
# -----------------------------

if st.session_state.portfolio["cash"] == 0:
    capital = st.number_input("💰 Capital inicial", min_value=0, value=1000000000)
    if st.button("Iniciar simulación"):
        st.session_state.portfolio["cash"] = capital
        st.session_state.portfolio["history"].append(capital)
        st.rerun()

portfolio = st.session_state.portfolio

# -----------------------------
# FUNCIONES FINANCIERAS
# -----------------------------

def buy(asset, amount, fecha):
    
    Acciones = amount / precio
    
    if amount > portfolio["cash"]:
        st.warning("No hay suficiente capital")
        return
    
    fecha_fin = fecha + timedelta(days=1)

    data = yf.download(asset, start=fecha, end=fecha_fin, progress=False)

    if data.empty:
        st.warning("No hay datos para esa fecha")
        return

    precio = data["Close"].iloc[0]

    rate = COMISIONES.get(asset, 0.002)
    commission = amount * rate
    
    portfolio["cash"] -= (amount + commission)
    
    portfolio["positions"][asset] = portfolio["positions"].get(asset, 0) + Acciones
    
    st.success(f"Compraste {amount:,.0f} en {asset} | Comisión: {commission:,.0f}")


def sell(asset, amount):
    if asset not in portfolio["positions"] or portfolio["positions"][asset] < amount:
        st.warning("No tienes suficiente posición")
        return
    
    rendimiento = np.random.uniform(-0.05, 0.05)
    valor_venta = amount * (1 + rendimiento)
    
    commission_rate = np.random.uniform(0.001, 0.002)
    commission = valor_venta * commission_rate
    
    portfolio["cash"] += (valor_venta - commission)
    portfolio["positions"][asset] -= amount
    
    st.success(
        f"Vendiste {amount:,.0f} en {asset} | "
        f"Retorno: {rendimiento*100:.2f}% | "
        f"Comisión: {commission:,.0f}"
    )


def total_value():

    total = portfolio["cash"]

    for asset, acciones in portfolio["positions"].items():
        try:
            data = yf.download(asset, period="1d", progress=False)
            precio_actual = data["Close"].iloc[-1]
            total += acciones * precio_actual
        except:
            pass

    return total

def update_history():
    value = total_value()
    portfolio["history"].append(value)


# -----------------------------
# INTERFAZ DE OPERACIONES
# -----------------------------

st.subheader("🧾 Operaciones")
fecha_operacion = st.date_input("📅 Selecciona la fecha de la operación")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🟢 Comprar")
    asset_buy = st.selectbox("Activo", list(COMISIONES.keys()), key="buy_asset")
    amount_buy = st.number_input("Monto a invertir", min_value=0, key="buy_amount")
    
    if st.button("Comprar"):
        buy(asset_buy, amount_buy)
        update_history()
        st.rerun()

with col2:
    st.markdown("### 🔴 Vender")
    asset_sell = st.selectbox("Activo", list(COMISIONES.keys()), key="sell_asset")
    amount_sell = st.number_input("Monto a vender", min_value=0, key="sell_amount")
    
    if st.button("Vender"):
        sell(asset_sell, amount_sell)
        update_history()
        st.rerun()

# -----------------------------
# ESTADO DEL PORTAFOLIO
# -----------------------------

st.subheader("📊 Estado del Portafolio")

col1, col2 = st.columns(2)

with col1:
    st.metric("💵 Efectivo", f"${portfolio['cash']:,.0f}")
    st.metric("📈 Valor Total", f"${total_value():,.0f}")

with col2:
    st.write("📦 Posiciones:")
    if portfolio["positions"]:
        df_positions = pd.DataFrame.from_dict(
            portfolio["positions"], orient="index", columns=["Acciones"]
        )
        st.dataframe(df_positions)
    else:
        st.info("Sin posiciones")

# -----------------------------
# GRÁFICO EN TIEMPO REAL
# -----------------------------

st.subheader(" Evolución del Portafolio")

if len(portfolio["history"]) > 1:
    fig, ax = plt.subplots()
    ax.plot(portfolio["history"])
    ax.set_title("Valor del Portafolio en el tiempo")
    ax.set_xlabel("Transacciones")
    ax.set_ylabel("Valor ($)")
    ax.grid()

    st.pyplot(fig)
else:
    st.info("Realiza operaciones para ver el gráfico")

# -----------------------------
# BOTÓN RESET
# -----------------------------

if st.button("🔄 Reiniciar simulación"):
    st.session_state.portfolio = {
        "cash": 0,
        "positions": {},
        "history": []
    }
    st.rerun()
