import streamlit as st
import requests
from pathlib import Path
from datetime import datetime


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Evandro & Eva - Vamos Comemorar!",
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

/* ============================================================
   FONTES
   ============================================================ */

@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Nunito:wght@400;600;700;800&display=swap');


/* ============================================================
   PÁGINA
   ============================================================ */

html,
body,
[class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 5% 5%,
            rgba(126, 164, 76, 0.45),
            transparent 22%
        ),
        radial-gradient(
            circle at 95% 15%,
            rgba(71, 121, 57, 0.50),
            transparent 25%
        ),
        radial-gradient(
            circle at 5% 90%,
            rgba(126, 83, 42, 0.30),
            transparent 25%
        ),
        linear-gradient(
            145deg,
            #163c27 0%,
            #245a32 45%,
            #326a39 75%,
            #1d472d 100%
        );

    background-attachment: fixed;
}


/* ============================================================
   STREAMLIT
   ============================================================ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* ============================================================
   CONTAINER
   ============================================================ */

.block-container {
    max-width: 720px;
    padding-top: 0.8rem;
    padding-bottom: 3rem;
    padding-left: 1rem;
    padding-right: 1rem;
}


/* ============================================================
   CONVITE
   ============================================================ */

.invite-wrapper {
    background: #fff6d9;
    padding: 7px;
    border-radius: 24px;
    border: 3px solid #ead49b;
    box-shadow: 0 12px 30px rgba(0,0,0,0.30);
    margin-bottom: 25px;
}


/* ============================================================
   CABEÇALHO
   ============================================================ */

.main-title {
    font-family: 'Baloo 2', sans-serif;
    font-size: 40px;
    font-weight: 800;
    text-align: center;

    color: #fff4c7;

    line-height: 1.05;

    margin-top: 12px;
    margin-bottom: 5px;

    text-shadow:
        2px 3px 0 #4a2915,
        0 4px 10px rgba(0,0,0,0.35);
}

.main-subtitle {
    text-align: center;

    color: #fff4c7;

    font-size: 18px;
    font-weight: 800;

    margin-bottom: 12px;

    text-shadow:
        1px 2px 0 #4a2915;
}

.event-info {
    text-align: center;

    color: #fff9e3;

    font-size: 16px;
    font-weight: 700;

    line-height: 1.7;

    margin-bottom: 25px;

    text-shadow:
        1px 2px 0 #4a2915;
}


/* ============================================================
   TÍTULOS
   ============================================================ */

.section-title {
    font-family: 'Baloo 2', sans-serif;

    color: #fff4c7;

    font-size: 30px;
    font-weight: 800;

    margin-top: 28px;
    margin-bottom: 4px;

    text-shadow:
        2px 3px 0 #4a2915,
        0 3px 8px rgba(0,0,0,0.25);
}

.section-description {
    color: #fff8e0;

    font-size: 15px;
    font-weight: 600;

    line-height: 1.45;

    margin-bottom: 12px;

    text-shadow:
        1px 2px 3px rgba(0,0,0,0.45);
}


/* ============================================================
   LABELS DOS CAMPOS
   ============================================================ */

label {
    color: #fff8e0 !important;
    font-weight: 700 !important;
}


/* ============================================================
   CAMPOS
   ============================================================ */

div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div,
div[data-baseweb="select"] > div {
    border-radius: 14px !important;
}


/* ============================================================
   PESSOA
   ============================================================ */

.person-header {
    background: linear-gradient(
        135deg,
        #7b4a25,
        #925d2c
    );

    color: white;

    border-radius: 16px;

    padding: 11px 16px;

    margin-top: 18px;
    margin-bottom: 8px;

    font-family: 'Baloo 2', sans-serif;

    font-size: 22px;
    font-weight: 800;

    box-shadow:
        0 5px 12px rgba(0,0,0,0.25);
}


/* ============================================================
   INFORMAÇÃO DE ADICIONAR
   ============================================================ */

.add-info {
    background: rgba(255, 231, 178, 0.96);

    color: #633817;

    border: 2px dashed #a86f36;

    border-radius: 17px;

    padding: 13px;

    margin-top: 18px;
    margin-bottom: 10px;

    text-align: center;

    font-weight: 800;

    box-shadow:
        0 5px 12px rgba(0,0,0,0.15);
}


/* ============================================================
   BOTÕES
   ============================================================ */

.stButton > button {
    border-radius: 15px !important;

    min-height: 48px !important;

    font-family: 'Nunito', sans-serif !important;

    font-size: 16px !important;

    font-weight: 800 !important;

    border: none !important;
}


/* ============================================================
   BOTÃO ADICIONAR
   ============================================================ */

.stButton > button:not([kind="primary"]) {
    background: #fff4d1 !important;

    color: #633817 !important;

    border: 2px solid #c58a4b !important;
}


/* ============================================================
   BOTÃO CONFIRMAR
   ============================================================ */

.stButton > button[kind="primary"] {
    background: linear-gradient(
        135deg,
        #8a4f20,
        #a8662d
    ) !important;

    color: white !important;

    font-family: 'Baloo 2', sans-serif !important;

    font-size: 22px !important;

    font-weight: 800 !important;

    min-height: 60px !important;

    box-shadow:
        0 6px 15px rgba(0,0,0,0.30);
}


/* ============================================================
   RADIO
   ============================================================ */

div[data-testid="stRadio"] label {
    color: #fff8e0 !important;

    font-size: 16px !important;

    font-weight: 700 !important;

    text-shadow:
        1px 2px 3px rgba(0,0,0,0.5);
}


/* ============================================================
   RODAPÉ
   ============================================================ */

.footer {
    text-align: center;

    color: #fff6d9;

    font-size: 14px;

    font-weight: 800;

    margin-top: 30px;

    padding-bottom: 25px;

    text-shadow:
        1px 2px 5px rgba(0,0,0,0.65);
}


/* ============================================================
   CELULAR
   ============================================================ */

@media (max-width: 600px) {

    .block-container {
        padding-left: 0.65rem;
        padding-right: 0.65rem;
        padding-top: 0.5rem;
    }

    .main-title {
        font-size: 32px;
    }

    .main-subtitle {
        font-size: 16px;
    }

    .event-info {
        font-size: 15px;
    }

    .section-title {
        font-size: 26px;
    }

    .section-description {
        font-size: 14px;
    }

    .person-header {
        font-size: 20px;
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
        '<div class="invite-wrapper">',
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
    '<div class="main-title">🦖 CONFIRME SUA PRESENÇA</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">🎉 Evandro & Eva vão comemorar!</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="event-info">
📅 <b>29 de novembro de 2026</b><br>
⏰ <b>12h</b><br>
📍 <b>Kids Planet Jundiaí</b>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# RESPONSÁVEL
# ============================================================

st.markdown(
    '<div class="section-title">👤 Quem está confirmando?</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Informe o nome do responsável pela confirmação.'
    '</div>',
    unsafe_allow_html=True
)

responsavel = st.text_input(
    "Nome do responsável",
    placeholder="Ex.: João da Silva",
    key="responsavel"
)


# ============================================================
# PESSOAS
# ============================================================

st.markdown(
    '<div class="section-title">👨‍👩‍👧 Quem vai participar?</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Adicione todas as pessoas que irão à festa.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# LISTA DE PESSOAS
# ============================================================

for i in range(len(st.session_state.people)):

    pessoa = st.session_state.people[i]

    st.markdown(
        f'<div class="person-header">👤 Pessoa {i + 1}</div>',
        unsafe_allow_html=True
    )

    nome = st.text_input(
        "Nome",
        value=pessoa["nome"],
        placeholder="Nome completo",
        key=f"nome_{i}"
    )

    st.session_state.people[i]["nome"] = nome

    col_idade, col_remover = st.columns([5, 1])

    with col_idade:

        idade = st.number_input(
            "Idade",
            min_value=0,
            max_value=120,
            value=int(pessoa["idade"]),
            step=1,
            key=f"idade_{i}"
        )

        st.session_state.people[i]["idade"] = idade

    with col_remover:

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
# ADICIONAR PESSOA
# ============================================================

st.markdown(
    """
<div class="add-info">
➕ Você pode adicionar todas as pessoas da família.
</div>
""",
    unsafe_allow_html=True
)

if st.button(
    "➕ Adicionar outra pessoa",
    use_container_width=True
):

    adicionar_pessoa()

    st.rerun()


# ============================================================
# STATUS
# ============================================================

st.markdown(
    '<div class="section-title">🎉 Você vai à festa?</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Escolha uma das opções abaixo.'
    '</div>',
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
    '<div class="section-title">💬 Deixe uma mensagem</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Opcional — mande um recado para o Evandro e a Eva.'
    '</div>',
    unsafe_allow_html=True
)

mensagem = st.text_area(
    "Mensagem (opcional)",
    placeholder="Ex.: Estamos muito felizes e ansiosos para comemorar!",
    height=110,
    key="mensagem"
)


# ============================================================
# BOTÃO CONFIRMAR
# ============================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True
)

enviar = st.button(
    "🎉 CONFIRMAR PRESENÇA",
    type="primary",
    use_container_width=True
)


# ============================================================
# ENVIO DOS DADOS
# ============================================================

if enviar:

    # --------------------------------------------------------
    # RESPONSÁVEL
    # --------------------------------------------------------

    if not responsavel.strip():

        st.error(
            "⚠️ Informe o nome do responsável."
        )

        st.stop()


    # --------------------------------------------------------
    # PESSOAS
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # DADOS
    # --------------------------------------------------------

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
    # ENVIO
    # ========================================================

    if script_url:
    try:
        response = requests.post(
            script_url,
            json=dados,
            timeout=15,
            allow_redirects=False
        )

        # O Google Apps Script pode responder com redirecionamento
        # mesmo quando recebeu e processou o POST corretamente.
        if response.status_code in (200, 201, 302, 303):
            st.success("Presença confirmada com sucesso! 🎉")
        else:
            st.error(
                f"Não foi possível enviar a confirmação. "
                f"Erro HTTP: {response.status_code}"
            )

    except Exception as e:
        st.error(f"Erro ao enviar confirmação: {e}")

# ============================================================
# RODAPÉ
# ============================================================

st.markdown(
    """
<div class="footer">
🦖 Evandro & Eva 🦕<br>
Obrigado por fazer parte desse momento! ❤️
</div>
""",
    unsafe_allow_html=True
)
