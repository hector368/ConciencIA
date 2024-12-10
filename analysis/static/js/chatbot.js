function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function enviarMensaje() {
    const mensaje = document.getElementById('mensaje').value.trim();
    if (!mensaje) {
        alert("Por favor, escribe un mensaje.");
        return;
    }

    // Agrega el mensaje del usuario
    agregarMensaje('user', mensaje);
    document.getElementById('mensaje').value = '';

    const csrftoken = getCookie('csrftoken');
    try {
        const response = await fetch('/chatbot_request/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
            },
            body: new URLSearchParams({ mensaje }),
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Error en la respuesta:', errorText);
            agregarMensaje('bot', 'Ocurrió un error al procesar tu solicitud.');
            return;
        }

        const data = await response.json();
        agregarMensaje('bot', data.respuesta || data.error);
    } catch (error) {
        console.error('Error en la solicitud:', error);
        agregarMensaje('bot', 'Ocurrió un error al procesar tu solicitud.');
    }
}

function agregarMensaje(tipo, mensaje) {
const contenedor = document.getElementById('messages');
const div = document.createElement('div');
div.className = tipo === 'user' ? 'user-message' : 'bot-message';
div.innerHTML = `<strong>${tipo === 'user' ? 'Tú:' : 'ConciencIA:'}</strong> ${mensaje}`;
contenedor.appendChild(div);
}

