import streamlit as st

st.set_page_config(
    page_title="Quantum Xavier",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
.big-title {
    font-size: 42px;
    font-weight: 700;
}
.subtitle {
    font-size: 18px;
    color: #9aa0a6;
}
.box {
    background: #111827;
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #1f2937;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">Quantum Xavier</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Sistema de análise institucional do mercado</div>', unsafe_allow_html=True)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="box">📊 Scanner de Mercado</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="box">🤖 Sinais da IA</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="box">📈 Estatísticas</div>', unsafe_allow_html=True)

st.write("")
st.success("Interface inicial carregada com sucesso.")
