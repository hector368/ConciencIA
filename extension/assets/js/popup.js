document.addEventListener('DOMContentLoaded', () => {
  chrome.storage.local.get('resultados', data => {
    const resultadosDiv = document.getElementById('resultados');
    resultadosDiv.innerHTML = ""; // Limpiar cualquier contenido previo

    if (data.resultados) {
      const { texto, insult, toxicity, threat, severe_toxicity } = data.resultados;

      // Crear el contenedor para mostrar los resultados
      const mensajeDiv = document.createElement('div');
      mensajeDiv.classList.add('mensaje');
      mensajeDiv.innerHTML = `
        <p><strong>Mensaje:</strong> ${texto}</p>
        <div class="nivel">
          <span>Insultos:</span> <span class="value">${Math.round(insult*100)}%</span>
        </div>
        <div class="nivel">
          <span>Toxicidad:</span> <span class="value">${Math.round(toxicity*100)}%</span>
        </div>
        <div class="nivel">
          <span>Amenaza:</span> <span class="value">${Math.round(threat*100)}%</span>
        </div>
        <div class="nivel">
          <span>Toxicidad Severa:</span> <span class="value">${Math.round(severe_toxicity*100)}%</span>
        </div>
      `;
      resultadosDiv.appendChild(mensajeDiv);
    } else {
      resultadosDiv.innerHTML = "<p>No hay resultados disponibles aún.</p>";
    }
  });
});
