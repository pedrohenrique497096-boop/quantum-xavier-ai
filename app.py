import streamlit as st
import pandas as pd

from core.scanner import scan
from config.settings import WATCHLIST, SYMBOL_NAMES

st.set_page_config(page_title="Quantum Xavier AI", layout="wide")

st.title("Quantum Xavier AI")

signals = []

for symbol in WATCHLIST:

    signal = scan(symbol)

    if signal:

        signal["symbol"] = SYMBOL_NAMES.get(symbol, symbol)

        signals.append(signal)

df = pd.DataFrame(signals)

st.subheader("Market Scanner")

if df.empty:

    st.info("Nenhum sinal encontrado no momento.")

else:

    st.dataframe(df)

    best = df.iloc[0]

    st.success(
        f"Sinal: {best['symbol']} | {best['direction']} | "
        f"Entrada: {best['entry']} | Stop: {best['stop']}"
    )
