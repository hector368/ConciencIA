// Función para iniciar el observador de mensajes en el chat actual
function iniciarObservadorMensajes() {
  // Detener cualquier observador anterior (si existe)
  if (window.mensajeObserver) {
    window.mensajeObserver.disconnect();
  }

  // Identificar el contenedor del chat principal
  const chatContainer = document.querySelector("div.x3psx0u.xwib8y2.xkhd6sd.xrmvbpv"); // Ajusta este selector si cambia
  if (chatContainer) {
    const mensajeObserver = new MutationObserver(mutations => {
      mutations.forEach(mutation => {
        mutation.addedNodes.forEach(node => {
          const nuevoMensaje = node.querySelector("span.selectable-text span");
          if (nuevoMensaje) {
            const texto = nuevoMensaje.innerText;

            // Enviar el texto del nuevo mensaje
            if (texto.trim()) {
              chrome.runtime.sendMessage({
                action: "sendText",
                text: texto
              });
              console.log("Nuevo mensaje enviado:", texto);
            } else {
              console.error("Mensaje vacío detectado.");
            }
          }
        });
      });
    });

    // Configurar el observer para monitorear cambios en el chat
    mensajeObserver.observe(chatContainer, { childList: true, subtree: true });

    console.log("Observer activado para detectar nuevos mensajes.");
    // Guardar el observer para detenerlo más adelante
    window.mensajeObserver = mensajeObserver;
  } else {
    console.error("No se encontró el contenedor del chat.");
  }
}

// Función para detectar cuando el usuario cambia de chat
function iniciarObservadorChats() {
  const listaChats = document.querySelector("div.x1y332i5.x1n2onr6.x6ikm8r.x10wlt62"); // Ajusta este selector si cambia

  if (listaChats) {
    const chatObserver = new MutationObserver(() => {
      console.log("Cambio de chat detectado. Reiniciando observador de mensajes.");
      setTimeout(() => {
        iniciarObservadorMensajes(); // Reiniciar el observador de mensajes
      }, 500); // Pequeña espera para asegurar que el DOM del chat está listo
    });

    // Configurar el observer para monitorear cambios en la lista de chats
    chatObserver.observe(listaChats, { childList: true, subtree: true });

    console.log("Observer activado para detectar cambios en la lista de chats.");
    // Guardar el observer para detenerlo más adelante si es necesario
    window.chatObserver = chatObserver;
  } else {
    console.error("No se encontró la lista de chats.");
  }
}

// Iniciar ambos observadores
iniciarObservadorChats();
iniciarObservadorMensajes();
