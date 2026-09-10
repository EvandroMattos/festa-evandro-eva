
/*
  GOOGLE APPS SCRIPT — banco gratuito da lista de convidados

  1) Crie uma planilha Google chamada "Festa Evandro e Eva".
  2) Extensões > Apps Script.
  3) Cole este código.
  4) Salve e faça Deploy > New deployment > Web app.
  5) Execute as: Me
  6) Who has access: Anyone
  7) Copie a URL /exec para o segredo GOOGLE_SCRIPT_URL no Streamlit.
*/

function doPost(e) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
    const data = JSON.parse(e.postData.contents);

    if (sheet.getLastRow() === 0) {
      sheet.appendRow([
        "Data/Hora", "Responsável", "Status",
        "Quantidade", "Nome", "Idade", "Mensagem"
      ]);
    }

    const pessoas = data.pessoas || [];

    pessoas.forEach(function(pessoa) {
      sheet.appendRow([
        data.timestamp || "",
        data.responsavel || "",
        data.status || "",
        data.quantidade || "",
        pessoa.nome || "",
        pessoa.idade || "",
        data.mensagem || ""
      ]);
    });

    return ContentService
      .createTextOutput(JSON.stringify({ok:true}))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ok:false, error:String(err)}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
