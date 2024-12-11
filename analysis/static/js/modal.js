// Obtén los elementos del DOM
const modal = document.getElementById('modal');
const closeModal = document.getElementById('close-modal');
const acceptBtn = document.getElementById('accept-btn');
const checkbox = document.getElementById('accept-checkbox');

// Muestra el modal cuando se carga la página
window.onload = function() {
    modal.style.display = "block";
};

// Cierra el modal cuando se hace clic en el "X"
closeModal.onclick = function() {
    modal.style.display = "none";
};

// Habilita el botón de aceptar cuando el checkbox esté marcado
checkbox.addEventListener('change', function() {
    if (checkbox.checked) {
        acceptBtn.disabled = false;
    } else {
        acceptBtn.disabled = true;
    }
});

// Cierra el modal y permite el uso de la extensión cuando se acepta
acceptBtn.onclick = function() {
    modal.style.display = "none";
    // Aquí podrías guardar el consentimiento del usuario en almacenamiento local si es necesario
}
