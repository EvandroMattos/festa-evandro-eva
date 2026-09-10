
# 🦖 Festa Evandro & Eva — RSVP

Aplicativo Streamlit para confirmação de presença da festa.

## Arquivos

- `app.py` — aplicativo
- `convite.png` — convite/arte visual
- `requirements.txt` — dependências
- `google_apps_script.gs` — endpoint gratuito para salvar as respostas em Google Sheets

## Publicação gratuita

1. Crie um repositório no GitHub e envie estes arquivos.
2. Entre em https://share.streamlit.io
3. Conecte sua conta GitHub.
4. Clique em Create app.
5. Escolha o repositório e `app.py`.
6. Faça o deploy.

O Streamlit Community Cloud oferece hospedagem gratuita para esse tipo de aplicação.

## Salvar confirmações

Crie uma Google Sheet, abra Extensões > Apps Script e use `google_apps_script.gs`.

Depois do deploy do Apps Script, copie a URL `/exec`.

No Streamlit, configure o Secret:

```toml
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/SEU_ID/exec"
```

Sem esse segredo, o app continua funcionando em modo demonstração e mostra o payload enviado.

## WhatsApp

Depois que o app estiver publicado, basta copiar a URL `*.streamlit.app` e enviar no WhatsApp junto com uma mensagem como:

"🦖🎉 Você está convidado para o aniversário do Evandro e da Eva! Confirme a presença da família pelo link: SEU_LINK"

## Observação

A aplicação é pública para os convidados. O endpoint do Google Apps Script deve ser usado apenas para receber os dados do formulário. Se você adicionar um painel administrativo, proteja-o com autenticação.
