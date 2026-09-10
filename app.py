import streamlit as st
import requests
from datetime import datetime


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Festa Evandro & Eva",
    page_icon="🦖",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# ESTADO DA APLICAÇÃO
# ============================================================

if "people" not in st.session_state:
    st.session_state.people = [
        {
            "nome": "",
            "idade": 5,
        }
    ]


# ============================================================
# FUNÇÕES
# ============================================================

def adicionar_pessoa():
    st.session_state.people.append(
        {
            "nome": "",
            "idade": 0,
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

@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700;800&family=Nunito:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(255,255,255,0.08), transparent 25%),
        radial-gradient(circle at 90% 20%, rgba(255,255,255,0.06), transparent 25%),
        linear-gradient(135deg, #174b29 0%, #236438 45%, #174b29 100%);
}

.block-container {
    max-width: 900px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

/* Esconde elementos desnecessários do Streamlit */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Imagem do convite */
.invitation {
    background: #fff2cf;
    border: 3px solid #d88a32;
    border-radius: 18px;
    padding: 8px;
    margin-bottom: 28px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
}

.invitation img {
    width: 100%;
    border-radius: 12px;
}

/* Títulos */
.party-title {
    font-family: 'Baloo 2', cursive;
    color: #fff4d0;
    font-size: 42px;
    font-weight: 800;
    line-height: 1.05;
    text-shadow:
        3px 3px 0 #633c20,
        5px 5px 10px rgba(0,0,0,0.35);
    margin-top: 22px;
    margin-bottom: 5px;
}

.party-subtitle {
    color: #fff8e5;
    font-size: 18px;
    font-weight: 700;
    text-shadow: 2px 2px 3px #3d2818;
    margin-bottom: 18px;
}

.section-title {
    font-family: 'Baloo 2', cursive;
    color: #fff4d0;
    font-size: 34px;
    font-weight: 800;
    line-height: 1.05;
    text-shadow:
        3px 3px 0 #633c20,
        4px 4px 8px rgba(0,0,0,0.35);
    margin-top: 28px;
    margin-bottom: 4px;
}

.section-description {
    color: #fff8e5;
    font-size: 17px;
    font-weight: 700;
    text-shadow: 2px 2px 3px #3d2818;
    margin-bottom: 15px;
}

/* Labels */
label {
    color: #fff8e5 !important;
    font-weight: 700 !important;
}

/* Campos */
div[data-baseweb="input"] {
    border-radius: 12px !important;
}

div[data-baseweb="textarea"] {
    border-radius: 12px !important;
}

/* Pessoa */
.person-box {
    background: rgba(255, 242, 207, 0.97);
    border: 3px solid #d88a32;
    border-radius: 18px;
    padding: 18px;
    margin-top: 12px;
    margin-bottom: 12px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.18);
}

.person-title {
    font-family: 'Baloo 2', cursive;
    color: #633c20;
    font-size: 25px;
    font-weight: 800;
    margin-bottom: 5px;
}

.person-info {
    color: #704b2c;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 10px;
}

/* Botão adicionar */
.add-info {
    text-align: center;
    color: #fff4d0;
    font-size: 14px;
    font-weight: 700;
    margin-top: 4px;
    margin-bottom: 4px;
}

/* Botões */
.stButton > button {
    border-radius: 14px !important;
    min-height: 48px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 16px !important;
    border: 2px solid #d88a32 !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #a95f22, #c8782b) !important;
    color: white !important;
    border: 2px solid #d88a32 !important;
    box-shadow: 0 5px 12px rgba(0,0,0,0.25) !important;
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #c8782b, #df8a34) !important;
}

/* Radio */
div[role="radiogroup"] {
    gap: 8px;
}

div[role="radiogroup"] label {
    color: #fff8e5 !important;
    font-size: 16px !important;
    font-weight: 700 !important;
}

/* Caixa de resultado */
.success-box {
    background: rgba(72, 125, 64, 0.75);
    border-radius: 12px;
    padding: 14px;
    color: white;
    font-weight: 800;
    text-align: center;
    margin-top: 15px;
}

.error-box {
    background: rgba(110, 67, 48, 0.65);
    border-radius: 12px;
    padding: 14px;
    color: #ffb5c7;
    font-weight: 800;
    text-align: center;
    margin-top: 15px;
}

/* Rodapé */
.footer {
    text-align: center;
    color: #fff4d0;
    font-family: 'Baloo 2', cursive;
    font-weight: 700;
    font-size: 18px;
    margin-top: 28px;
    margin-bottom: 10px;
    text-shadow: 2px 2px 3px #3d2818;
}

/* Mobile */
@media (max-width: 600px) {

    .block-container {
        padding-left: 14px;
        padding-right: 14px;
        padding-top: 0.8rem;
    }

    .party-title {
        font-size: 34px;
    }

    .section-title {
        font-size: 29px;
    }

    .section-description {
        font-size: 15px;
    }

    .person-box {
        padding: 14px;
    }

    .invitation {
        padding: 5px;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# CONVITE
# ============================================================

st.markdown(
    '<div class="invitation">',
    unsafe_allow_html=True,
)

try:
    st.image(
        "convite.png",
        use_container_width=True,
    )
except Exception:
    st.warning(
        "A imagem convite.png não foi encontrada no projeto."
    )

st.markdown(
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    '<div class="party-title">🎉 Você vai à festa?</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="party-subtitle">Escolha uma das opções abaixo.</div>',
    unsafe_allow_html=True,
)


# ============================================================
# RESPONSÁVEL
# ============================================================

st.markdown(
    '<div class="section-title">👨‍👩‍👧‍👦 Quem está respondendo?</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">Informe o nome do responsável pela confirmação.</div>',
    unsafe_allow_html=True,
)

responsavel = st.text_input(
    "Nome do responsável",
    placeholder="Ex.: João da Silva",
)


# ============================================================
# PARTICIPANTES
# ============================================================

st.markdown(
    '<div class="section-title">🦖 Quem vai participar?</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">Adicione cada pessoa que irá à festa.</div>',
    unsafe_allow_html=True,
)


for index, pessoa in enumerate(st.session_state.people):

    st.markdown(
        f"""
<div class="person-box">
<div class="person-title">👤 Pessoa {index + 1}</div>
<div class="person-info">
Informe o nome e a idade.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([3, 1])

    with col1:
        pessoa["nome"] = st.text_input(
            f"Nome da pessoa {index + 1}",
            value=pessoa["nome"],
            key=f"nome_{index}",
            placeholder="Nome",
        )

    with col2:
        pessoa["idade"] = st.number_input(
            f"Idade",
            min_value=0,
            max_value=120,
            value=int(pessoa["idade"]),
            step=1,
            key=f"idade_{index}",
        )

    if len(st.session_state.people) > 1:

        if st.button(
            "🗑️ Remover",
            key=f"remove_{index}",
        ):
            remover_pessoa(index)
            st.rerun()


# ============================================================
# ADICIONAR PESSOA
# ============================================================

st.markdown(
    '<div class="add-info">Você pode adicionar mais familiares ou convidados.</div>',
    unsafe_allow_html=True,
)

if st.button(
    "➕ Adicionar outra pessoa",
    key="add_person",
):
    adicionar_pessoa()
    st.rerun()


# ============================================================
# STATUS
# ============================================================

st.markdown(
    '<div class="section-title">🎉 Você vai à festa?</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">Escolha uma das opções abaixo.</div>',
    unsafe_allow_html=True,
)

status = st.radio(
    "Escolha uma opção:",
    [
        "✅ Sim, estaremos lá!",
        "❌ Infelizmente não poderemos ir.",
    ],
    index=0,
)


# ============================================================
# MENSAGEM
# ============================================================

st.markdown(
    '<div class="section-title">💬 Deixe uma mensagem</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">Opcional — mande um recado para o Evandro e a Eva.</div>',
    unsafe_allow_html=True,
)

mensagem = st.text_area(
    "Mensagem (opcional)",
    placeholder="Escreva uma mensagem...",
    height=120,
)


# ============================================================
# ENVIO
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

enviar = st.button(
    "🎉 CONFIRMAR PRESENÇA",
    type="primary",
    use_container_width=True,
)


if enviar:

    # --------------------------------------------------------
    # Validação do responsável
    # --------------------------------------------------------

    if not responsavel.strip():

        st.error(
            "Por favor, informe o nome do responsável."
        )

        st.stop()


    # --------------------------------------------------------
    # Pessoas válidas
    # --------------------------------------------------------

    pessoas_validas = []

    for pessoa in st.session_state.people:

        nome = pessoa["nome"].strip()

        if nome:

            pessoas_validas.append(
                {
                    "nome": nome,
                    "idade": int(pessoa["idade"]),
                }
            )


    if not pessoas_validas:

        st.error(
            "Informe pelo menos uma pessoa que irá à festa."
        )

        st.stop()


    # --------------------------------------------------------
    # Dados enviados para o Google Sheets
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
        "mensagem": mensagem.strip(),
    }


    # --------------------------------------------------------
    # URL do Google Apps Script
    # --------------------------------------------------------

    script_url = st.secrets.get(
        "GOOGLE_SCRIPT_URL",
        ""
    )


    # --------------------------------------------------------
    # Envio para Google Sheets
    # --------------------------------------------------------

    if script_url:

        try:

            response = requests.post(
                script_url,
                json=dados,
                timeout=20,
                allow_redirects=True,
            )


            # Google Apps Script normalmente retorna
            # HTTP 200 quando a execução termina.
            if response.status_code == 200:

                st.markdown(
                    """
<div class="success-box">
🎉 Presença confirmada com sucesso!<br>
Obrigado por fazer parte desse momento! ❤️
</div>
""",
                    unsafe_allow_html=True,
                )

            else:

                st.error(
                    "Não foi possível enviar a confirmação. "
                    f"Erro HTTP: {response.status_code}"
                )

                # Mostra uma informação útil para diagnóstico
                with st.expander("Detalhes técnicos"):

                    st.write(
                        "Status HTTP:",
                        response.status_code,
                    )

                    st.write(
                        "Resposta:",
                        response.text[:1000],
                    )


        except requests.exceptions.Timeout:

            st.error(
                "O envio demorou demais e expirou. "
                "Tente novamente."
            )


        except requests.exceptions.RequestException as e:

            st.error(
                "Erro de comunicação com o Google Sheets."
            )

            with st.expander("Detalhes técnicos"):
                st.write(str(e))


        except Exception as e:

            st.error(
                "Ocorreu um erro inesperado ao enviar a confirmação."
            )

            with st.expander("Detalhes técnicos"):
                st.write(str(e))


    # --------------------------------------------------------
    # Fallback caso não exista o Secret
    # --------------------------------------------------------

    else:

        st.success(
            "Formulário funcionando!"
        )

        st.info(
            "O Google Sheets ainda não está conectado."
        )

        st.json(dados)


# ============================================================
# RODAPÉ
# ============================================================

st.markdown(
    """
<div class="footer">
🦕 Evandro & Eva 🦕<br>
Obrigado por fazer parte desse momento! ❤️
</div>
""",
    unsafe_allow_html=True,
)
