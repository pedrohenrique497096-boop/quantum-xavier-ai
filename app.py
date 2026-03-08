import streamlit as st
import pandas as pd

from config.settings import APP_TITLE, WATCHLIST, MIN_CONFIDENCE
from core.scanner import scan
from core.database import setup, save_signal, load_signals

setup()

st.set_page_config(
    page_title=APP_TITLE,
    layout="wide"
)

st.title(APP_TITLE)
st.caption("Scanner de mercado com análise automática para Forex, Ouro e Crypto.")

if "saved_signatures" not in st.session_state:
    st.session_state.saved_signatures = set()

col1, col2, col3 = st.columns(3)
col1.metric("Ativos monitorados", len(WATCHLIST))
col2.metric("Confiança mínima", f"{MIN_CONFIDENCE}")
col3.metric("Status", "Online")

signals = []

with st.spinner("Analisando mercado..."):
    for symbol in WATCHLIST:
        signal = scan(symbol)
        if signal:
            signature = (
                signal["symbol"],
                signal["direction"],
                round(signal["entry"], 8),
                round(signal["stop"], 8),
                round(signal["target"], 8),
            )

            signals.append(signal)

            if signature not in st.session_state.saved_signatures:
                save_signal(signal)
                st.session_state.saved_signatures.add(signature)

if signals:
    df = pd.DataFrame(signals).sort_values("confidence", ascending=False).reset_index(drop=True)

    st.subheader("Melhores sinais da rodada")
    st.dataframe(
        df[["symbol", "direction", "entry", "stop", "target", "confidence", "reason"]],
        use_container_width=True
    )

    best = df.iloc[0]

    st.success(
        f"Melhor sinal: {best['symbol']} | {best['direction']} | "
        f"Entrada: {best['entry']:.5f} | Stop: {best['stop']:.5f} | "
        f"Alvo: {best['target']:.5f} | Confiança: {best['confidence']:.2f}"
    )
else:
    st.warning("Nenhum sinal forte encontrado nesta rodada.")

st.subheader("Histórico salvo")
history = load_signals(limit=50)

if history is not None and not history.empty:
    st.dataframe(history, use_container_width=True)
else:
    st.info("Ainda não há histórico salvo.")
