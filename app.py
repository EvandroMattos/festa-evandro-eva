from pathlib import Path
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Festa Evandro & Eva",
    page_icon="🦖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Nunito:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}
.stApp {
    background:
      linear-gradient(rgba(15,32,18,.82), rgba(15,32,18,.92)),
      url("https://images.unsplash.com/photo-1518709594023-6eab9bab7b23?auto=format&fit=crop&w=1200&q=85");
    background-size: cover;
    background-attachment: fixed;
}
.block-container {
    max-width: 760px;
    padding: 1rem .8rem 3rem;
}
.hero {
    border-radius: 28px;
    overflow: hidden;
    box-shadow: 0 18px 50px rgba(0,0,0,.45);
    margin-bottom: 18px;
}
.hero img { width: 100%; display:block; }
.wood-card {
    background: linear-gradient(145deg, rgba(66,40,22,.97), rgba(36,25,16,.97));
    border: 3px solid rgba(205,155,84,.55);
    border-radius: 28px;
    padding: 24px 22px;
    box-shadow: 0 16px 45px rgba(0,0,0,.42);
    color: white;
}
.title {
    font-family:'Baloo 2', cursive;
    font-size: 2.25rem;
    font-weight: 800;
    text-align:center;
    margin:0;
    line-height:1;
}
.subtitle {
    text-align:center;
    color:#f8e7d1;
    font-size:1.02rem;
    margin:7px 0 20px;
}
.section {
    font-family:'Baloo 2', cursive;
    font-size:1.35rem;
    font-weight:800;
    margin:20px 0 8px;
}
.info {
    background: rgba(255,255,255,.08);
    border-radius:18px;
    padding:14px 12px;
    text-align:center;
    margin-bottom:14px;
}
.big-number {
    font-family:'Baloo 2', cursive;
    font-size:2rem;
    font-weight:800;
    color:#ff91c5;
}
.stButton > button {
    width:100%;
    border-radius:18px;
    border:0;
    padding: .85rem 1rem;
    font-family:'Baloo 2', cursive;
    font-size:1.2rem;
    font-weight:800;
    background: linear-gradient(90deg,#ff5fa8,#ff8fc4);
    color:white;
    box-shadow:0 7px 0 #b52e68;
}
.stButton > button:hover { color:white; transform:translateY(-1px); }
label, .stTextInput label, .stNumberInput label, .stSelectbox label {
    color:white !important;
    font-weight:800 !important;
}
div[data-baseweb="input"], div[data-baseweb="select"] {
    border-radius:14px;
}
.footer {
    text-align:center;
    color:#f3d9bf;
    margin-top:20px;
    font-size:.9rem;
}
</style>
""", unsafe_allow_html=True)

# Invitation image supplied by the user
if Path("convite.png").exists():
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.image("convite.png", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="wood-card">
  <div class="title">🦖 CONFIRME SUA PRESENÇA</div>
  <div class="subtitle">Será uma alegria ter você com a gente nesse dia especial!</div>
</div>
""", unsafe_allow_html=True)

st.write("")

with st.form("rsvp_form", clear_on_submit=False):
    nome_responsavel = st.text_input("Nome do responsável *", placeholder="Digite seu nome")
    quantidade = st.number_input(
        "Quantas pessoas da sua família irão? *",
        min_value=1, max_value=20, value=1, step=1
    )

    st.markdown('<div class="section">👨‍👩‍👧 Integrantes da família</div>', unsafe_allow_html=True)

    pessoas = []
    for i in range(int(quantidade)):
        c1, c2 = st.columns([3,1])
        with c1:
            nome = st.text_input(
                f"Nome {i+1} *",
                key=f"nome_{i}",
                placeholder="Nome completo"
            )
        with c2:
            idade = st.number_input(
                f"Idade {i+1} *",
                min_value=0, max_value=120, value=1,
                key=f"idade_{i}"
            )
        pessoas.append((nome.strip(), int(idade)))

    st.markdown('<div class="section">🎉 Você confirma a presença?</div>', unsafe_allow_html=True)
    confirma = st.radio(
        "Escolha uma opção",
        ["Sim, vamos participar!", "Não poderemos ir"],
        horizontal=True
    )

    mensagem = st.text_area(
        "💌 Algum recado para os aniversariantes? (opcional)",
        placeholder="Deixe uma mensagem..."
    )

    enviado = st.form_submit_button("🦖 ENVIAR CONFIRMAÇÃO")

if enviado:
    erros = []
    if not nome_responsavel.strip():
        erros.append("Informe o nome do responsável.")
    if any(not nome for nome, _ in pessoas):
        erros.append("Informe o nome de todos os integrantes.")

    if erros:
        for erro in erros:
            st.error(erro)
    else:
        payload = {
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "responsavel": nome_responsavel.strip(),
            "status": "CONFIRMADO" if confirma.startswith("Sim") else "NÃO VAI",
            "quantidade": int(quantidade),
            "pessoas": [{"nome": n, "idade": a} for n, a in pessoas],
            "mensagem": mensagem.strip(),
        }

        script_url = st.secrets.get("GOOGLE_SCRIPT_URL", "")
        if script_url:
            try:
                r = requests.post(script_url, json=payload, timeout=15)
                if r.ok:
                    st.success("🎉 Presença registrada com sucesso! Até lá!")
                    st.balloons()
                else:
                    st.error("Não foi possível registrar agora. Tente novamente em alguns instantes.")
            except Exception:
                st.error("Não foi possível conectar ao sistema de confirmações. Tente novamente.")
        else:
            st.warning(
                "O aplicativo está funcionando em modo de demonstração. "
                "Configure GOOGLE_SCRIPT_URL para salvar as confirmações."
            )
            st.json(payload)

st.markdown("""
<div class="wood-card" style="margin-top:20px">
  <div class="info">
    <div class="big-number">29/11/2026 • 12h</div>
    📍 Kids Planet Jundiaí<br>
    Rua Atílio Vianelo, 233 — Vila Vianelo, Jundiaí
  </div>
  <div style="text-align:center;font-size:1.15rem;font-weight:800">
    🦕 Brincadeiras, dinossauros e muita diversão! 💕
  </div>
</div>
<div class="footer">🌿 Até lá! 🦖</div>
""", unsafe_allow_html=True)
