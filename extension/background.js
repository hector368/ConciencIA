chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "sendText") {
    const texto = message.text;

    // URL del servidor Django (usando 127.0.0.1 en lugar de localhost)
    const apiUrl = "http://127.0.0.1:8000/api/analyze/";

    // Enviar el texto al servidor Django
    fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: texto })
    })
      .then(response => response.json())
      .then(data => {
        console.log('Respuesta del servidor:', data);

        // Guardar solo el mensaje más reciente
        chrome.storage.local.set({
          resultados: { 
            texto,
            insult: data.insult,
            toxicity: data.toxicity,
            threat: data.threat,
            severe_toxicity: data.severe_toxicity
          }
        });
      })
      .catch(error => console.error('Error al enviar el texto:', error));
  }
});
