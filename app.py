import streamlit as st
import requests
from pathlib import Path
from datetime import datetime


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Evandro & Eva — Vamos Comemorar!",
    page_icon="🦖",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# ESTADO DA LISTA DE PESSOAS
# ============================================================

if "people" not in st.session_state:
    st.session_state.people = [
        {
            "nome": "",
            "idade": 1
        }
    ]


def adicionar_pessoa():
    st.session_state.people.append(
        {
            "nome": "",
            "idade": 1
        }
    )


def remover_pessoa(index):
    if len(st.session_state.people) > 1:
        st.session_state.people.pop(index)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ==============================
       IMPORTAÇÃO DAS FONTES
       ============================== */

    @import url(
        'https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700;800&family=Nunito:wght@400;500;600;700;800&display=swap'
    );


    /* ==============================
       CONFIGURAÇÃO GERAL
       ============================== */

    html,
    body,
    [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    .stApp {
        background:
            linear-gradient(
                rgba(20, 30, 10, 0.25),
                rgba(20, 30, 10, 0.25)
            ),
            url(
                "https://images.unsplash.com/photo-1518709594023-6eab9bab7b23?auto=format&fit=crop&w=1600&q=85"
            );

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }


    /* ==============================
       ESCONDER MENU E FOOTER
       ============================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* ==============================
       CONTAINER PRINCIPAL
       ============================== */

    .block-container {
        max-width: 760px;
        padding-top: 1rem;
        padding-bottom: 3rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }


    /* ==============================
       CARD
       ============================== */

    .card {
        background: rgba(255, 248, 225, 0.97);
        border-radius: 28px;
        padding: 28px;
        margin-top: 20px;
        margin-bottom: 20px;

        box-shadow:
            0 12px 35px rgba(0, 0, 0, 0.25);

        border: 4px solid rgba(110, 75, 35, 0.25);
    }


    /* ==============================
       TÍTULO
       ============================== */

    .hero-title {
        font-family: 'Baloo 2', sans-serif;
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        color: #5d351c;
        line-height: 1.05;
        margin-bottom: 8px;
    }

    .hero-sub {
        font-family: 'Nunito', sans-serif;
        font-size: 18px;
        font-weight: 700;
        text-align: center;
        color: #704b2a;
        margin-bottom: 12px;
    }


    /* ==============================
       TÍTULOS DAS SEÇÕES
       ============================== */

    .section-title {
        font-family: 'Baloo 2', sans-serif;
        font-size: 27px;
        font-weight: 800;
        color: #5d351c;
        margin-top: 10px;
        margin-bottom: 5px;
    }


    /* ==============================
       TEXTO
       ============================== */

    .description {
        color: #684a31;
        font-size: 15px;
        line-height: 1.5;
        margin-bottom: 15px;
    }


    /* ==============================
       CARD DE CADA PESSOA
       ============================== */

    .person-card {
        background: #fffdf5;
        border: 2px solid #dcc7a4;
        border-radius: 20px;
        padding: 16px;
        margin-bottom: 12px;

        box-shadow:
            0 4px 12px rgba(80, 50, 20, 0.08);
    }

    .person-title {
        font-family: 'Baloo 2', sans-serif;
        font-size: 21px;
        font-weight: 800;
        color: #5d351c;
        margin-bottom: 8px;
    }


    /* ==============================
       BOTÃO ADICIONAR
       ============================== */

    .add-box {
        background: #f3e3bd;
        border: 2px dashed #a87b43;
        border-radius: 18px;
        padding: 14px;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 20px;
    }


    /* ==============================
       INPUTS
       ============================== */

    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        border-radius: 14px !important;
    }

    div[data-baseweb="select"] > div {
        border-radius: 14px !important;
    }


    /* ==============================
       BOTÕES
       ============================== */

    .stButton > button {
        border-radius: 15px !important;
        font-family: 'Nunito', sans-serif !important;
        font-weight: 800 !important;
        min-height: 48px !important;
    }


    /* ==============================
       BOTÃO PRINCIPAL
       ============================== */

    .primary-button {
        background: #7a4b25;
        color: white;
        border-radius: 18px;
        padding: 15px;
        text-align: center;
        font-family: 'Baloo 2', sans-serif;
        font-size: 23px;
        font-weight: 800;
        margin-top: 15px;
    }


    /* ==============================
       CONVITE
       ============================== */

    .invite {
        background: white;
        padding: 8px;
        border-radius: 25px;
        box-shadow:
            0 12px 30px rgba(0, 0, 0, 0.25);
        margin-bottom: 20px;
        overflow: hidden;
    }


    /* ==============================
       RODAPÉ
       ============================== */

    .footer-text {
        text-align: center;
        color: white;
        font-size: 13px;
        font-weight: 700;
        text-shadow:
            0 2px 4px rgba(0, 0, 0, 0.7);

        margin-top: 20px;
    }


    /* ==============================
       MOBILE
       ============================== */

    @media (max-width: 600px) {

        .block-container {
            padding-left: 0.6rem;
            padding-right: 0.6rem;
            padding-top: 0.5rem;
        }

        .card {
            padding: 18px;
            border-radius: 22px;
        }

        .hero-title {
            font-size: 32px;
        }

        .hero-sub {
            font-size: 16px;
        }

        .section-title {
            font-size: 24px;
        }

        .description {
            font-size: 14px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CONVITE
# ============================================================

imagem_convite = Path("convite.png")

if imagem_convite.exists():

    st.markdown(
        '<div class="invite">',
        unsafe_allow_html=True
    )

    st.image(
        str(imagem_convite),
        use_container_width=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    """
    <div class="card">

        <div class="hero-title">
            🦖 CONFIRME SUA PRESENÇA
        </div>

        <div class="hero-sub">
            🎉 Evandro & Eva vão comemorar!
        </div>

        <div style="text-align:center; color:#704b2a;">
            📅 <b>29 de novembro de 2026</b><br>
            ⏰ <b>12h</b><br>
            📍 <b>Kids Planet Jundiaí</b>
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FORMULÁRIO
# ============================================================

st.markdown(
    """
    <div class="card">

        <div class="section-title">
            👨‍👩‍👧 Quem vai participar?
        </div>

        <div class="description">
            Primeiro informe o nome do responsável e depois
            adicione todas as pessoas da família que irão à festa.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# RESPONSÁVEL
# ============================================================

responsavel = st.text_input(
    "👤 Nome do responsável",
    placeholder="Ex.: João da Silva",
    key="responsavel"
)


# ============================================================
# PESSOAS
# ============================================================

st.markdown(
    """
    <div class="section-title">
        👨‍👩‍👧 Pessoas que irão
    </div>
    """,
    unsafe_allow_html=True
)


for i in range(len(st.session_state.people)):

    pessoa = st.session_state.people[i]

    st.markdown(
        f"""
        <div class="person-card">

            <div class="person-title">
                👤 Pessoa {i + 1}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([5, 2, 1])

    with col1:

        nome = st.text_input(
            "Nome",
            value=pessoa["nome"],
            placeholder="Nome completo",
            key=f"nome_{i}"
        )

        st.session_state.people[i]["nome"] = nome

    with col2:

        idade = st.number_input(
            "Idade",
            min_value=0,
            max_value=120,
            value=int(pessoa["idade"]),
            step=1,
            key=f"idade_{i}"
        )

        st.session_state.people[i]["idade"] = idade

    with col3:

        st.write("")

        if len(st.session_state.people) > 1:

            if st.button(
                "🗑️",
                key=f"remover_{i}",
                help="Remover esta pessoa"
            ):

                remover_pessoa(i)
                st.rerun()


# ============================================================
# ADICIONAR OUTRA PESSOA
# ============================================================

st.markdown(
    """
    <div class="add-box">
        ➕ Você pode adicionar quantas pessoas quiser.
    </div>
    """,
    unsafe_allow_html=True
)


if st.button(
    "➕  Adicionar outra pessoa",
    use_container_width=True
):

    adicionar_pessoa()
    st.rerun()


# ============================================================
# CONFIRMAÇÃO
# ============================================================

st.markdown(
    """
    <div class="card">

        <div class="section-title">
            🎉 Você vai à festa?
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


status = st.radio(
    "Escolha uma opção:",
    [
        "✅ Sim, estaremos lá!",
        "❌ Infelizmente não poderemos ir."
    ],
    key="status"
)


# ============================================================
# MENSAGEM
# ============================================================

st.markdown(
    """
    <div class="section-title">
        💬 Deixe uma mensagem
    </div>
    """,
    unsafe_allow_html=True
)


mensagem = st.text_area(
    "Mensagem (opcional)",
    placeholder="Ex.: Estamos muito felizes e ansiosos para comemorar!",
    height=100,
    key="mensagem"
)


# ============================================================
# BOTÃO ENVIAR
# ============================================================

st.markdown(
    """
    <div class="primary-button">
        🎉 Enviar confirmação
    </div>
    """,
    unsafe_allow_html=True
)


enviar = st.button(
    "CONFIRMAR PRESENÇA",
    use_container_width=True
)


# ============================================================
# ENVIO DOS DADOS
# ============================================================

if enviar:

    # --------------------------------------------
    # VALIDAÇÃO DO RESPONSÁVEL
    # --------------------------------------------

    if not responsavel.strip():

        st.error(
            "⚠️ Por favor, informe o nome do responsável."
        )

        st.stop()


    # --------------------------------------------
    # VALIDAÇÃO DOS NOMES
    # --------------------------------------------

    pessoas_validas = []

    for pessoa in st.session_state.people:

        nome = pessoa["nome"].strip()

        if not nome:

            st.error(
                "⚠️ Preencha o nome de todas as pessoas."
            )

            st.stop()

        pessoas_validas.append(
            {
                "nome": nome,
                "idade": int(pessoa["idade"])
            }
        )


    # --------------------------------------------
    # MONTA OS DADOS
    # --------------------------------------------

    dados = {

        "timestamp": datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        ),

        "responsavel": responsavel.strip(),

        "status": (
            "CONFIRMADO"
            if status.startswith("✅")
            else "NÃO VAI"
        ),

        "quantidade": len(pessoas_validas),

        "pessoas": pessoas_validas,

        "mensagem": mensagem.strip()
    }


    # ========================================================
    # GOOGLE APPS SCRIPT
    # ========================================================

    try:

        script_url = st.secrets.get(
            "GOOGLE_SCRIPT_URL",
            ""
        )

    except Exception:

        script_url = ""


    # ========================================================
    # ENVIA PARA GOOGLE SHEETS
    # ========================================================

    if script_url:

        try:

            resposta = requests.post(
                script_url,
                json=dados,
                timeout=15
            )

            if resposta.ok:

                st.success(
                    "🎉 Presença enviada com sucesso!"
                )

                st.balloons()

            else:

                st.error(
                    "❌ Não foi possível enviar a confirmação."
                )

        except Exception as erro:

            st.error(
                "❌ Erro ao conectar com o Google Sheets."
            )

            st.caption(
                f"Detalhes: {erro}"
            )


    # ========================================================
    # SEM GOOGLE SHEETS AINDA
    # ========================================================

    else:

        st.success(
            "🎉 Formulário funcionando!"
        )

        st.info(
            "📊 O Google Sheets ainda não está conectado."
        )

        st.write("Dados que serão enviados:")

        st.json(dados)


# ============================================================
# RODAPÉ
# ============================================================

st.markdown(
    """
    <div class="footer-text">
        🦖 Evandro & Eva 🦕<br>
        Obrigado por fazer parte desse momento! ❤️
    </div>
    """,
    unsafe_allow_html=True
)
