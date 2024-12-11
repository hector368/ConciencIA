chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "sendText") {
    const texto = message.text;

    // URL del servidor Django
    const apiUrl = "https://conciencia.onrender.com/api/analyze/";

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
        var level = 0.60 ;

        if (resultados.insult > level) {
          high_level = "insultante";
          send_notification(high_level,resultados);
        }
        
        if (resultados.toxicity > level) {
          high_level = "toxico";
          send_notification(high_level, resultados);
        }
        
        if (resultados.threat > level) {
          high_level = "amenazante";
          send_notification(high_level, resultados);
        }
        
        if (resultados.severe_toxicity > level) {
          high_level = "severamente toxico";
          send_notification(high_level, resultados);
        }

      })
      .catch(error => console.error('Error al enviar el texto:', error));
  }
});


function send_notification(high_level, resultados) {
  // Formatear el mensaje para la notificación
  const notificacionMensaje = `Se ha detectado un mensaje ${high_level}: ${resultados.texto}`;

  // Generar una ID única para la notificación
  const notificationId = `notificacion_${Date.now()}`;

  // Mostrar la notificación
  const notificationsApi = chrome.notifications || browser.notifications; // Compatibilidad Chrome/Firefox
  notificationsApi.create(notificationId, {
      type: 'basic',
      iconUrl: 'icon.png', // Asegúrate de tener este ícono
      title: '¿Necesitas ayuda?',
      message: notificacionMensaje,
  });

  // Escuchar clics en la notificación
  notificationsApi.onClicked.addListener((id) => {
      if (id === notificationId) {
          console.log("Se pulso la notificacion");
          // Redirigir al sitio web con el mensaje como atributo
          const mensaje = encodeURIComponent(resultados.texto); // Asegúrate de codificar el texto
          const url = `https://conciencia.onrender.com/chatbot?mensaje=He recibido el siguiente mensaje:${mensaje}`;
          // Usar chrome.tabs.create o browser.tabs.create para abrir una nueva pestaña
          const tabsApi = chrome.tabs || browser.tabs;
          tabsApi.create({ url: url }, (tab) => {
              console.log("Nueva pestaña abierta:", tab);
          });
      }
  });
}
