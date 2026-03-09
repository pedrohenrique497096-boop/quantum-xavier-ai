import streamlit as st
from core.scanner import scan

st.set_page_config(
    page_title="Quantum Xavier AI",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>

body {
background-color:#0e1117;
}

.big-title{
font-size:42px;
font-weight:700;
color:white;
}

.subtitle{
font-size:18px;
color:#9aa0a6;
}

.main-card{
background:#111827;
padding:30px;
border-radius:15px;
border:1px solid #1f2937;
}

</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1,3])

with col1:
    st.image("assets/logo.png", width=150)

with col2:
    st.markdown('<div class="big-title">Quantum Xavier</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Sistema de análise institucional do mercado</div>', unsafe_allow_html=True)

st.divider()

if st.button("🚀 Rodar análise do mercado"):

    results = scan()

    if len(results) == 0:
        st.warning("Nenhum sinal encontrado no momento")

    else:

        st.success("Sinais encontrados")

        st.dataframe(results)
