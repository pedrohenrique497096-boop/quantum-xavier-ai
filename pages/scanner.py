import streamlit as st
from core.scanner import scan
import pandas as pd

st.title("Scanner de Mercado")

if st.button("Atualizar Scanner"):

    data = scan()

    if len(data) == 0:
        st.warning("Nenhum ativo com sinal")

    else:

        df = pd.DataFrame(data)

        st.dataframe(df)

        for _, row in df.iterrows():

            st.metric(
                label=row["symbol"],
                value=f"{row['confidence']}% confiança"
            )
