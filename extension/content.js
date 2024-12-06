
// Usar MutationObserver para detectar mensajes nuevos en tiempo real
const chatContainer = document.querySelector("div.x3psx0u"); // Ajusta este selector si cambia

if (chatContainer) {
  const observer = new MutationObserver(mutations => {
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
  observer.observe(chatContainer, { childList: true, subtree: true });

  console.log("Observer activado para detectar nuevos mensajes.");
} else {
  console.error("No se encontró el contenedor del chat.");
}