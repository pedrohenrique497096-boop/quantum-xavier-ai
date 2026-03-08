import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from config.settings import APP_TITLE, WATCHLIST, MIN_CONFIDENCE, TOP_N_SIGNALS
from core.database import (
    setup,
    open_signal_exists,
    save_open_signal,
    load_open_signals,
    load_closed_signals,
    close_signal,
    stats_summary,
)
from core.scanner import scan


setup()

st.set_page_config(page_title=APP_TITLE, layout="wide")
st.title(APP_TITLE)
st.caption("Scanner automático para Forex, Ouro e Crypto com sinais, gráfico e histórico.")

# =========================
# Funções auxiliares
# =========================

def check_open_signals():
    open_df = load_open_signals()
    if open_df is None or open_df.empty:
        return

    for _, row in open_df.iterrows():
        signal, df = scan(row["symbol"])
        if df is None or df.empty:
            continue

        last = df.iloc[-1]
        high_ = float(last["High"])
        low_ = float(last["Low"])

        direction = row["direction"]
        stop = float(row["stop"])
        target = float(row["target"])
        signal_id = int(row["id"])

        if direction == "BUY":
            if low_ <= stop:
                close_signal(signal_id, "STOP")
            elif high_ >= target:
                close_signal(signal_id, "TAKE")

        elif direction == "SELL":
            if high_ >= stop:
                close_signal(signal_id, "STOP")
            elif low_ <= target:
                close_signal(signal_id, "TAKE")


def make_chart(df, signal=None, symbol=""):
    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name=symbol
        )
    )

    if signal is not None:
        fig.add_hline(y=signal["entry"], line_dash="dash", annotation_text="Entrada")
        fig.add_hline(y=signal["stop"], line_dash="dash", annotation_text="Stop")
        fig.add_hline(y=signal["target"], line_dash="dash", annotation_text="Alvo")

    fig.update_layout(
        height=520,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
    )
    return fig


# =========================
# Atualização de sinais
# =========================

check_open_signals()

# =========================
# Scanner
# =========================

signals = []
chart_df = None
best_signal = None

with st.spinner("Analisando ativos..."):
    for symbol in WATCHLIST:
        signal, df = scan(symbol)
        if signal is not None:
            signals.append(signal)
            if not open_signal_exists(signal):
                save_open_signal(signal)

if signals:
    signals_df = pd.DataFrame(signals).sort_values("confidence", ascending=False).head(TOP_N_SIGNALS).reset_index(drop=True)
    best_signal = signals_df.iloc[0].to_dict()
    _, chart_df = scan(best_signal["symbol"])
else:
    signals_df = pd.DataFrame()

# =========================
# Métricas
# =========================

stats = stats_summary()
m1, m2, m3, m4 = st.columns(4)
m1.metric("Status", "On-line")
m2.metric("Confiança mínima", f"{MIN_CONFIDENCE}")
m3.metric("Sinais abertos", stats["open"])
m4.metric("Win rate", f"{stats['winrate']:.1f}%")

# =========================
# Melhor sinal + gráfico
# =========================

left, right = st.columns([1.2, 1])

with left:
    st.subheader("Melhores pares da rodada")
    if not signals_df.empty:
        st.dataframe(
            signals_df[["symbol", "direction", "entry", "stop", "target", "confidence", "reason"]],
            use_container_width=True
        )
    else:
        st.warning("Nenhum sinal forte encontrado nesta rodada.")

with right:
    st.subheader("Melhor sinal")
    if best_signal is not None:
        st.success(
            f"{best_signal['symbol']} | {best_signal['direction']} | "
            f"Entrada: {best_signal['entry']:.5f} | "
            f"Parada: {best_signal['stop']:.5f} | "
            f"Alvo: {best_signal['target']:.5f} | "
            f"Confiança: {best_signal['confidence']:.2f}"
        )
        st.info(best_signal["reason"])
    else:
        st.info("Sem sinal líder nesta rodada.")

if best_signal is not None and chart_df is not None:
    st.subheader(f"Gráfico do ativo: {best_signal['symbol']}")
    st.plotly_chart(make_chart(chart_df, best_signal, best_signal["symbol"]), use_container_width=True)

# =========================
# Históricos
# =========================

open_col, closed_col = st.columns(2)

with open_col:
    st.subheader("Sinais abertos")
    open_df = load_open_signals()
    if open_df is not None and not open_df.empty:
        st.dataframe(open_df, use_container_width=True)
    else:
        st.info("Nenhum sinal aberto.")

with closed_col:
    st.subheader("Histórico encerrado")
    closed_df = load_closed_signals(limit=100)
    if closed_df is not None and not closed_df.empty:
        st.dataframe(closed_df, use_container_width=True)
    else:
        st.info("Nenhum sinal encerrado ainda.")
