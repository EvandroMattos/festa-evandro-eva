import streamlit as st
import requests
from pathlib import Path
from datetime import datetime

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Evandro & Eva — Vamos Comemorar!",
    page_icon="🦖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CONTROLE DAS PESSOAS
# ============================================================

if "people" not in st.session_state:
    st.session_state.people = [
        {
            "nome": "",
            "idade": 1
        }
    ]


def adicionar_pessoa():
    st.session_state.people.append({
        "nome": "",
        "idade": 1
    })


def remover_pessoa(index):
    if len(st.session_state.people) > 1:
        st.session_state.people.pop(index)


# ============================================================
# ESTILO
# ============================================================

st.markdown("""
<style>

@import url(
    'https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Nunito:wght@400;600;700;800;900&display=swap'
);

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {

    background:
        linear-gradient(
            rgba(10, 28, 17, .84),
            rgba(10, 28, 17, .94)
        ),
        url(
            "https://images.unsplash.com/photo-1518709594023-6eab9bab7b23?auto=format&fit=crop&w=1400&q=85"
        );

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.block-container {

    max-width: 820px;

    padding-top: .8rem;
    padding-left: .65rem;
    padding-right: .65rem;
    padding-bottom: 3rem;
}


/* ----------------------------------------------------------
   CONVITE
---------------------------------------------------------- */

.invite {

    border-radius: 26px;

    overflow: hidden;

    box-shadow:
        0 18px 55px rgba(0,0,0,.5);

    margin-bottom: 18px;
}

.invite img {

    display: block;

    width: 100%;
}


/* ----------------------------------------------------------
   CARD
---------------------------------------------------------- */

.card {

    background:
        linear-gradient(
            145deg,
            rgba(64,38,20,.98),
            rgba(32,22,14,.98)
        );

    border:
        2px solid rgba(210,163,96,.62);

    border-radius: 28px;

    padding: 22px 20px;

    box-shadow:
        0 16px 45px rgba(0,0,0,.45);

    color: white;
}


/* ----------------------------------------------------------
   TÍTULOS
---------------------------------------------------------- */

.hero-title {

    font-family: 'Baloo 2', cursive;

    font-size: 2.35rem;

    line-height: 1;

    text-align: center;

    font-weight: 800;

    margin: 0;
}

.hero-sub {

    text-align: center;

    color: #ffe9d4;

    font-size: 1.02rem;

    margin-top: 8px;
}

.section-title {

    font-family: 'Baloo 2', cursive;

    font-size: 1.5rem;

    font-weight: 800;

    margin:
        19px 0 8px;
}

.helper {

    color: #f8dfc7;

    font-size: .94rem;

    margin-bottom: 8px;
}


/* ----------------------------------------------------------
   PESSOA
---------------------------------------------------------- */

.person-card {

    background:
        rgba(255,255,255,.075);

    border:
        1px solid rgba(255,255,255,.12);

    border-radius: 18px;

    padding:
        11px 10px 4px;

    margin:
        8px 0;
}

.person-number {

    font-weight: 900;

    color: #ffd9b4;

    margin:
        0 0 2px 3px;
}


/* ----------------------------------------------------------
   BOTÃO ADICIONAR
---------------------------------------------------------- */

.add-box {

    border:
        2px dashed rgba(139,207,69,.8);

    border-radius: 16px;

    padding: 3px;

    margin:
        9px 0 4px;
}


/* ----------------------------------------------------------
   BOTÕES
---------------------------------------------------------- */

.stButton > button {

    border-radius: 16px;

    min-height: 46px;

    font-family: 'Baloo 2', cursive;

    font-weight: 800;

    font-size: 1.08rem;
}

.primary-btn button {

    background:
        linear-gradient(
            90deg,
            #f56fae,
            #ff9acb
        ) !important;

    color: white !important;

    border: 0 !important;

    box-shadow:
        0 5px 0 #b93670;
}

.add-btn button {

    background:
        transparent !important;

    color:
        #b7ee76 !important;

    border:
        2px solid #8bcf45 !important;
}

.remove-btn button {

    background:
        rgba(245,111,174,.12) !important;

    color:
        #ff9acb !important;

    border:
        1px solid rgba(245,111,174,.35) !important;
}


/* ----------------------------------------------------------
   INPUTS
---------------------------------------------------------- */

div[data-baseweb="input"],
div[data-baseweb="select"],
textarea {

    border-radius: 14px !important;
}

label {

    color: white !important;

    font-weight: 800 !important;
}


/* ----------------------------------------------------------
   INFORMAÇÕES DA FESTA
---------------------------------------------------------- */

.info {

    text-align: center;

    background:
        rgba(255,255,255,.07);

    border-radius: 18px;

    padding: 13px;

    margin-top: 15px;
}

.info strong {

    font-size: 1.2rem;
}


/* ----------------------------------------------------------
   RODAPÉ
---------------------------------------------------------- */

.footer {

    text-align: center;

    color: #ffe4cc;

    margin-top: 16px;

    font-weight: 700;
}


/* ----------------------------------------------------------
   CELULAR
---------------------------------------------------------- */

@media (max-width: 600px) {

    .block-container {

        padding-left: .5rem;

        padding-right: .5rem;
    }

    .card {

        padding:
            18px 14px;

        border-radius: 23px;
    }

    .hero-title {

        font-size: 2rem;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# IMAGEM DO CONVITE
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
# TÍTULO
# ============================================================

st.markdown("""
<div class="card">

    <div class="hero-title">
        🦖 CONFIRME SUA PRESENÇA
    </div>

    <div class="hero-sub">
        Será uma alegria ter você com a gente nesse dia especial!
    </div>

</div>
""", unsafe_allow_html=True)

st.write("")


# ============================================================
# FORMULÁRIO
# ============================================================

st.markdown(
    '<div class="card">',
    unsafe_allow_html=True
)


# RESPONSÁVEL

responsavel = st.text_input(
    "Nome do responsável *",
    placeholder="Ex.: João da Silva",
    key="responsavel"
)


# ============================================================
# PESSOAS
# ============================================================

st.markdown(
    '<div class="section-title">👨‍👩‍👧‍👦 Quem vai participar?</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="helper">
        Adicione cada pessoa que irá à festa,
        incluindo adultos, crianças e bebês.
    </div>
    """,
    unsafe_allow_html=True
)


for i in range(len(st.session_state.people)):

    pessoa = st.session_state.people[i]

    st.markdown(
        f"""
        <div class="person-card">
            <div class="person-number">
                Pessoa {i + 1}
            </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(
        [5, 2, 1]
    )

    # NOME

    with col1:

        pessoa["nome"] = st.text_input(
            "Nome",

            value=pessoa["nome"],

            key=f"nome_{i}",

            placeholder="Nome completo",

            label_visibility="collapsed"
        )


    # IDADE

    with col2:

        pessoa["idade"] = st.number_input(
            "Idade",

            min_value=0,

            max_value=120,

            value=int(pessoa["idade"]),

            step=1,

            key=f"idade_{i}",

            label_visibility="collapsed"
        )


    # REMOVER

    with col3:

        if len(st.session_state.people) > 1:

            if st.button(
                "🗑️",
                key=f"remover_{i}",
                help="Remover esta pessoa"
            ):

                remover_pessoa(i)

                st.rerun()


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# ADICIONAR PESSOA
# ============================================================

st.markdown(
    '<div class="add-box">',
    unsafe_allow_html=True
)

if st.button(
    "➕  Adicionar outra pessoa",
    use_container_width=True
):

    adicionar_pessoa()

    st.rerun()

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# CONFIRMAÇÃO
# ============================================================

st.markdown(
    '<div class="section-title">🎉 Você confirma a presença?</div>',
    unsafe_allow_html=True
)

status = st.radio(
    "Escolha uma opção",

    [
        "✅ Sim, vamos participar!",
        "❌ Não poderemos ir"
    ],

    horizontal=True,

    label_visibility="collapsed"
)


# ============================================================
# MENSAGEM
# ============================================================

mensagem = st.text_area(

    "💌 Algum recado para os aniversariantes? (opcional)",

    placeholder="Deixe uma mensagem carinhosa...",

    height=90
)


# ============================================================
# ENVIAR
# ============================================================

st.markdown(
    '<div class="primary-btn">',
    unsafe_allow_html=True
)

enviar = st.button(
    "🦖  ENVIAR CONFIRMAÇÃO",
    use_container_width=True
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# PROCESSAMENTO
# ============================================================

if enviar:

    erros = []


    if not responsavel.strip():

        erros.append(
            "Informe o nome do responsável."
        )


    for i, pessoa in enumerate(
        st.session_state.people
    ):

        if not pessoa["nome"].strip():

            erros.append(
                f"Informe o nome da Pessoa {i + 1}."
            )


    # ERROS

    if erros:

        for erro in erros:

            st.error(erro)


    # ENVIO

    else:

        dados = {

            "timestamp":
                datetime.now().strftime(
                    "%d/%m/%Y %H:%M:%S"
                ),

            "responsavel":
                responsavel.strip(),

            "status":
                (
                    "CONFIRMADO"
                    if status.startswith("✅")
                    else "NÃO VAI"
                ),

            "quantidade":
                len(st.session_state.people),

            "pessoas": [

                {
                    "nome":
                        pessoa["nome"].strip(),

                    "idade":
                        int(pessoa["idade"])
                }

                for pessoa
                in st.session_state.people
            ],

            "mensagem":
                mensagem.strip()
        }


        # URL DO GOOGLE SHEETS

        script_url = st.secrets.get(
            "GOOGLE_SCRIPT_URL",
            ""
        )


        # SE GOOGLE SHEETS ESTIVER CONFIGURADO

        if script_url:

            try:

                resposta = requests.post(

                    script_url,

                    json=dados,

                    timeout=15
                )


                if resposta.ok:

                    st.success(
                        "🎉 Confirmação registrada! "
                        "Obrigado e até a festa!"
                    )

                    st.balloons()


                else:

                    st.error(
                        "Não conseguimos registrar "
                        "agora. Tente novamente."
                    )


            except Exception:

                st.error(
                    "Não conseguimos conectar "
                    "ao sistema. Tente novamente."
                )


        # MODO DE TESTE

        else:

            st.success(
                "🎉 Formulário funcionando! "
                "O Google Sheets ainda não está conectado."
            )

            st.json(dados)


# ============================================================
# INFORMAÇÕES DA FESTA
# ============================================================

st.markdown("""
<div class="card">

    <div class="info">

        <strong>
            📅 29/11/2026 • 12h
        </strong>

        <br>

        📍 Kids Planet Jundiaí

        <br>

        Rua Atílio Vianelo, 233 —
        Vila Vianelo, Jundiaí

    </div>


    <div class="footer">

        🦕 Brincadeiras,
        dinossauros e muita diversão! 💕

        <br>

        Até lá! 🦖

    </div>

</div>
""", unsafe_allow_html=True)
