document.addEventListener('DOMContentLoaded', () => {
  chrome.storage.local.get('resultados', data => {
    const resultadosDiv = document.getElementById('resultados');
    resultadosDiv.textContent = ""; // Limpiar cualquier contenido previo

    if (data.resultados) {
      const { texto, insult, toxicity, threat, severe_toxicity } = data.resultados;

      // Crear el contenedor para mostrar los resultados
      const mensajeDiv = document.createElement('div');
      mensajeDiv.classList.add('mensaje');

      // Crear el elemento para mostrar el texto del mensaje
      const mensajeP = document.createElement('p');
      const mensajeStrong = document.createElement('strong');
      mensajeStrong.textContent = "Mensaje: ";
      mensajeP.appendChild(mensajeStrong);
      mensajeP.appendChild(document.createTextNode(texto));
      mensajeDiv.appendChild(mensajeP);

      // Crear y añadir niveles dinámicamente
      const niveles = [
        { label: "Insultos", value: insult },
        { label: "Toxicidad", value: toxicity },
        { label: "Amenaza", value: threat },
        { label: "Toxicidad Severa", value: severe_toxicity }
      ];

      niveles.forEach(nivel => {
        const nivelDiv = document.createElement('div');
        nivelDiv.classList.add('nivel');

        const labelSpan = document.createElement('span');
        labelSpan.textContent = `${nivel.label}:`;

        const valueSpan = document.createElement('span');
        valueSpan.classList.add('value');
        valueSpan.textContent = `${Math.round(nivel.value * 100)}%`;

        nivelDiv.appendChild(labelSpan);
        nivelDiv.appendChild(valueSpan);
        mensajeDiv.appendChild(nivelDiv);
      });

      resultadosDiv.appendChild(mensajeDiv);
    } else {
      const noResultadosP = document.createElement('p');
      noResultadosP.textContent = "No hay resultados disponibles aún.";
      resultadosDiv.appendChild(noResultadosP);
    }
  });
});
