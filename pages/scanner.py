import streamlit as st
import pandas as pd
from core.scanner import scan

st.set_page_config(page_title="Scanner", layout="wide")

st.title("📊 Scanner de Mercado")
st.write("Ativos analisados pela Quantum Xavier.")

if st.button("Atualizar Scanner"):
    data = scan()

    if not data:
        st.warning("Nenhum ativo com sinal")
    else:
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

        st.subheader("Resumo")
        for _, row in df.iterrows():
            st.metric(
                label=row.get("symbol", "Ativo"),
                value=f"{row.get('confidence', 0)}% confiança"
            )
