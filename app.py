import streamlit as st
import pandas as pd

from core.scanner import scan
from config.settings import WATCHLIST
from core.database import setup, save_signal

setup()

st.set_page_config(page_title="Quantum Xavier AI", layout="wide")

st.title("Quantum Xavier Market AI")

signals = []

for symbol in WATCHLIST:

    signal = scan(symbol)

    if signal:

        signals.append(signal)

        if signal["confidence"] > 70:
            save_signal(signal)

df = pd.DataFrame(signals)

st.subheader("Melhores sinais")

st.dataframe(df.sort_values("confidence", ascending=False))

if len(df):

    best = df.sort_values("confidence", ascending=False).iloc[0]

    st.success(f"""
Melhor sinal agora

Ativo: {best.symbol}

Direção: {best.direction}

Entrada: {best.entry}

Stop: {best.stop}

Alvo: {best.target}

Confiança: {best.confidence}
""")
