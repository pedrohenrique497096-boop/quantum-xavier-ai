import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from core.scanner import scan

st.set_page_config(page_title="Quantum Xavier AI", layout="wide")

st.title("Terminal de IA Quantum Xavier")

st.write("Sistema de análise institucional do mercado")

if st.button("Rodar análise do mercado"):

    data = scan()

    if isinstance(data, list) and len(data) > 0:

        df = pd.DataFrame(data)

        st.subheader("Sinais encontrados")

        st.dataframe(df)

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=df["symbol"],
                y=df["confidence"],
                name="Confiança da IA"
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    else:

        st.warning("Nenhum sinal encontrado no momento")
