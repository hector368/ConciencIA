chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "sendText") {
    const texto = message.text;

    // URL del servidor Django
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

        // Crear los resultados
        const resultados = {
          texto,
          insult: data.insult,
          toxicity: data.toxicity,
          threat: data.threat,
          severe_toxicity: data.severe_toxicity,
        };

        chrome.storage.local.set({ resultados });


        var high_level = "";

        if (resultados.insult > 0.70) {
          high_level = "insultante";
          send_notification(high_level,resultados);
        }
        
        if (resultados.toxicity > 0.70) {
          high_level = "toxico";
          send_notification(high_level, resultados);
        }
        
        if (resultados.threat > 0.70) {
          high_level = "amenazante";
          send_notification(high_level, resultados);
        }
        
        if (resultados.severe_toxicity > 0.70) {
          high_level = "severamente toxico";
          send_notification(high_level, resultados);
        }

      })
      .catch(error => console.error('Error al enviar el texto:', error));
  }
});


function send_notification(high_level,resultados) {
          // Formatear el mensaje para la notificación
          const notificacionMensaje = `Se ha detectado un mensaje ${high_level}: ${resultados.texto}`;

        // Mostrar la notificación
        const notificationsApi = chrome.notifications || browser.notifications; // Compatibilidad Chrome/Firefox
        notificationsApi.create({
          type: 'basic',
          iconUrl: 'icon.png', // Asegúrate de tener este ícono
          title: '¿Necesitas ayuda?',
          message: notificacionMensaje,
        });
  
}