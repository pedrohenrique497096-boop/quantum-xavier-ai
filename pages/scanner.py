import streamlit as st
from core.scanner import scan

st.set_page_config(page_title="Scanner", layout="wide")

st.title("📊 Scanner de Mercado")
st.write("Ativos analisados pela Quantum Xavier.")

if st.button("Atualizar Scanner"):

    data = scan()

    if not data:
        st.warning("Nenhum ativo com sinal")

    else:

        cols = st.columns(3)

        for i, asset in enumerate(data):

            col = cols[i % 3]

            with col:

                symbol = asset.get("symbol", "Ativo")
                confidence = asset.get("confidence", 0)
                side = asset.get("side", "N/A")

                color = "#16c784" if side == "BUY" else "#ea3943"

                st.markdown(
                    f"""
                    <div style="
                    background-color:#111827;
                    padding:20px;
                    border-radius:12px;
                    border:1px solid #1f2937;
                    margin-bottom:20px">

                    <h3 style="color:white">{symbol}</h3>

                    <p style="color:#9ca3af">
                    Direção: <span style="color:{color}">{side}</span>
                    </p>

                    <p style="color:#9ca3af">
                    Confiança IA: <b>{confidence}%</b>
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )
