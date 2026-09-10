import streamlit as st
import requests
from pathlib import Path
from datetime import datetime


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Evandro & Eva - Vamos Comemorar!",
    page_icon="🦖",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# ESTADO
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

@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Nunito:wght@400;500;600;700;800&display=swap');


/* ==========================================================
   PÁGINA
   ========================================================== */

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(112, 151, 72, 0.45),
            transparent 25%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(38, 91, 48, 0.60),
            transparent 30%
        ),
        radial-gradient(
            circle at 15% 90%,
            rgba(130, 83, 40, 0.35),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #173b27 0%,
            #285d36 45%,
            #3f6e3b 75%,
            #594029 100%
        );

    background-attachment: fixed;
}


/* ==========================================================
   ESCONDER ELEMENTOS STREAMLIT
   ========================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* ==========================================================
   CONTAINER
   ========================================================== */

.block-container {
    max-width: 720px;
    padding-top: 1rem;
    padding-bottom: 3rem;
    padding-left: 1rem;
    padding-right: 1rem;
}


/* ==========================================================
   CONVITE
   ========================================================== */

.invite-card {
    background: #fff9e7;
    padding: 7px;
    border-radius: 25px;
    border: 4px solid rgba(255, 239, 190, 0.95);
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.35);
    margin-bottom: 25px;
    overflow: hidden;
}


/* ==========================================================
   CARDS
   ========================================================== */

.form-card {
    background: rgba(255, 248, 225, 0.98);
    border-radius: 24px;
    padding: 22px;
    margin-top: 18px;
    margin-bottom: 18px;
    border: 4px solid rgba(116, 79, 38, 0.25);
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.25);
}


/* ==========================================================
   TÍTULOS
   ========================================================== */

.main-title {
    font-family: 'Baloo 2', sans-serif;
    font-size: 38px;
    font-weight: 800;
    text-align: center;
    color: #5c351c;
    line-height: 1.05;
    margin-bottom: 8px;
}

.main-subtitle {
    font-size: 17px;
    font-weight: 800;
    text-align: center;
    color: #704728;
    margin-bottom: 12px;
}

.event-info {
    text-align: center;
    color: #704728;
    font-size: 16px;
    line-height: 1.7;
}

.section-title {
    font-family: 'Baloo 2', sans-serif;
    font-size: 27px;
    font-weight: 800;
    color: #5c351c;
    margin-bottom: 5px;
}

.section-description {
    color: #705238;
    font-size: 15px;
    line-height: 1.5;
}


/* ==========================================================
   PESSOA
   ========================================================== */

.person-header {
    background: #76502d;
    color: white;
    border-radius: 15px;
    padding: 10px 15px;
    margin-top: 14px;
    margin-bottom: 10px;

    font-family: 'Baloo 2', sans-serif;
    font-size: 21px;
    font-weight: 800;
}


/* ==========================================================
   BOTÕES
   ========================================================== */

.stButton > button {
    border-radius: 15px !important;
    min-height: 48px !important;

    font-family: 'Nunito', sans-serif !important;
    font-size: 16px !important;
    font-weight: 800 !important;
}


/* ==========================================================
   BOTÃO PRINCIPAL
   ========================================================== */

.stButton > button[kind="primary"] {
    background: #75451f !important;
    color: white !important;
    border: none !important;

    font-family: 'Baloo 2', sans-serif !important;
    font-size: 21px !important;
    font-weight: 800 !important;

    min-height: 58px !important;

    box-shadow:
        0 5px 12px rgba(0, 0, 0, 0.25);
}


/* ==========================================================
   AVISO ADICIONAR
   ========================================================== */

.add-info {
    background: #f1dfb6;
    border: 2px dashed #a8783d;
    color: #704728;

    border-radius: 16px;
    padding: 12px;

    text-align: center;

    font-size: 14px;
    font-weight: 700;

    margin-top: 12px;
    margin-bottom: 10px;
}


/* ==========================================================
   INPUTS
   ========================================================== */

div[data-baseweb="input"] > div {
    border-radius: 13px !important;
}

div[data-baseweb="textarea"] > div {
    border-radius: 13px !important;
}

div[data-baseweb="select"] > div {
    border-radius: 13px !important;
}


/* ==========================================================
   RODAPÉ
   ========================================================== */

.footer {
    text-align: center;
    color: white;

    font-size: 14px;
    font-weight: 800;

    text-shadow:
        0 2px 5px rgba(0, 0, 0, 0.7);

    padding-top: 15px;
    padding-bottom: 25px;
}


/* ==========================================================
   CELULAR
   ========================================================== */

@media (max-width: 600px) {

    .block-container {
        padding-left: 0.6rem;
        padding-right: 0.6rem;
        padding-top: 0.5rem;
    }

    .form-card {
        padding: 18px;
        border-radius: 21px;
    }

    .main-title {
        font-size: 31px;
    }

    .main-subtitle {
        font-size: 16px;
    }

    .event-info {
        font-size: 15px;
    }

    .section-title {
        font-size: 24px;
    }

    .section-description {
        font-size: 14px;
    }

    .person-header {
        font-size: 19px;
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
        '<div class="invite-card">',
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
    '<div class="form-card">',
    unsafe_allow_html=True
)

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

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# RESPONSÁVEL
# ============================================================

st.markdown(
    '<div class="form-card">',
    unsafe_allow_html=True
)

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

st.markdown(
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
    '<div class="form-card">',
    unsafe_allow_html=True
)

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

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# CADA PESSOA
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
                help="Remover pessoa"
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
# PRESENÇA
# ============================================================

st.markdown(
    '<div class="form-card">',
    unsafe_allow_html=True
)

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

st.markdown(
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
    '<div class="form-card">',
    unsafe_allow_html=True
)

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

st.markdown(
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
# BOTÃO
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

enviar = st.button(
    "🎉 CONFIRMAR PRESENÇA",
    type="primary",
    use_container_width=True
)


# ============================================================
# ENVIO
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


    # --------------------------------------------------------
    # GOOGLE SCRIPT
    # --------------------------------------------------------

    try:

        script_url = st.secrets.get(
            "GOOGLE_SCRIPT_URL",
            ""
        )

    except Exception:

        script_url = ""


    # --------------------------------------------------------
    # ENVIO PARA GOOGLE SHEETS
    # --------------------------------------------------------

    if script_url:

        try:

            resposta = requests.post(
                script_url,
                json=dados,
                timeout=15
            )

            if resposta.ok:

                st.success(
                    "🎉 Presença confirmada com sucesso!"
                )

                st.balloons()

            else:

                st.error(
                    "❌ Não foi possível enviar a confirmação."
                )

        except Exception:

            st.error(
                "❌ Erro ao conectar com o sistema de confirmação."
            )


    # --------------------------------------------------------
    # TESTE SEM GOOGLE SHEETS
    # --------------------------------------------------------

    else:

        st.success(
            "🎉 Formulário funcionando!"
        )

        st.info(
            "📊 O Google Sheets ainda não está conectado."
        )

        st.json(dados)


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
