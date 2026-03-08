
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

API_URL = "https://quantum-xavier-ai.onrender.com/scan"

st.set_page_config(
    page_title="Quantum Xavier AI",
    layout="wide"
)

st.title("Quantum Xavier AI Terminal")

if st.button("Rodar análise do mercado"):

    response = requests.get(API_URL)

    data = response.json()

    if isinstance(data, list) and len(data) > 0:

        df = pd.DataFrame(data)

        st.subheader("Sinais encontrados")

        st.dataframe(df)

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=df["symbol"],
                y=df["confidence"],
                name="Confiança"
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    else:

        st.warning("Nenhum sinal encontrado")
