import streamlit as st
import plotly.graph_objects as go

from config.settings import APP_TITLE
from core.scanner import scan_all, evaluate_open_trades
from data.market import get_data
from ai.model import explain_signal
from analytics.heatmap import market_heatmap
from database.trades import (
    setup_db,
    open_trade_exists,
    save_open_trade,
    load_open_trades,
    load_closed_trades,
    stats_summary,
)
from backtest.simulator import monte_carlo_equity

st.set_page_config(page_title=APP_TITLE, layout="wide")

setup_db()
evaluate_open_trades()

st.title(APP_TITLE)
st.caption("Análise top-down D1 → H1 → M5 com travamento de mercado, histórico e gestão de sinais.")

signals = scan_all()

valid_signals = signals[
    (signals["direction"].isin(["BUY", "SELL"])) &
    (signals["entry"].notna())
].copy() if not signals.empty else signals

for _, row in valid_signals.iterrows():
    signal_dict = row.to_dict()
    if not open_trade_exists(signal_dict["symbol"], signal_dict["direction"]):
        save_open_trade(signal_dict)

stats = stats_summary()
heat = market_heatmap(valid_signals)
sim_equity = monte_carlo_equity(winrate=max(stats["winrate"] / 100, 0.5))

m1, m2, m3, m4 = st.columns(4)
m1.metric("Status", "On-line")
m2.metric("Sinais abertos", stats["open"])
m3.metric("Win rate", f"{stats['winrate']}%")
m4.metric("Monte Carlo", f"${sim_equity}")

st.write(f"Heatmap | Compradores: {heat['buy']} | Vendedores: {heat['sell']}")

left, right = st.columns([1.15, 1])

with left:
    st.subheader("Todos os ativos analisados")
    if signals.empty:
        st.warning("Nenhum ativo analisado.")
    else:
        st.dataframe(
            signals[[
                "display_symbol",
                "market_status",
                "direction",
                "entry",
                "stop",
                "target",
                "confidence",
                "reason",
            ]],
            use_container_width=True,
        )

with right:
    st.subheader("Melhor sinal")
    if valid_signals.empty:
        st.info("Nenhum sinal válido neste momento.")
    else:
        best = valid_signals.iloc[0].to_dict()
        st.success(
            f"{best['display_symbol']} | {best['direction']} | "
            f"Entrada: {best['entry']:.5f} | "
            f"Stop: {best['stop']:.5f} | "
            f"Alvo: {best['target']:.5f} | "
            f"Confiança: {best['confidence']:.2f}"
        )
        st.info(explain_signal(best))

        chart_df = get_data(best["symbol"], "5m", 200)
        if chart_df is not None and not chart_df.empty:
            fig = go.Figure(
                data=[
                    go.Candlestick(
                        x=chart_df.index,
                        open=chart_df["Open"],
                        high=chart_df["High"],
                        low=chart_df["Low"],
                        close=chart_df["Close"],
                        name=best["display_symbol"],
                    )
                ]
            )

            fig.add_hline(y=best["entry"], line_dash="dash", annotation_text="Entrada")
            fig.add_hline(y=best["stop"], line_dash="dash", annotation_text="Stop")
            fig.add_hline(y=best["target"], line_dash="dash", annotation_text="Alvo")

            fig.update_layout(
                height=500,
                template="plotly_dark",
                xaxis_rangeslider_visible=False,
                margin=dict(l=10, r=10, t=30, b=10),
            )

            st.plotly_chart(fig, use_container_width=True)

open_col, closed_col = st.columns(2)

with open_col:
    st.subheader("Sinais abertos")
    open_df = load_open_trades()
    if open_df.empty:
        st.info("Nenhum sinal aberto.")
    else:
        st.dataframe(open_df, use_container_width=True)

with closed_col:
    st.subheader("Histórico encerrado")
    closed_df = load_closed_trades()
    if closed_df.empty:
        st.info("Nenhum trade encerrado ainda.")
    else:
        st.dataframe(closed_df, use_container_width=True)
