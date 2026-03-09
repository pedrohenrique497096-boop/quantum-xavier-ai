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

                st.markdown(
                    f"""
                    ### {asset.get("symbol","Ativo")}

                    **Confiança:** {asset.get("confidence",0)}%

                    **Direção:** {asset.get("side","N/A")}
                    """
                )
