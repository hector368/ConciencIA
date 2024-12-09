import openai
from dotenv import load_dotenv
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
import os

# Cargar las variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def chatbot_view(request):
    """
    Vista para manejar solicitudes al chatbot enfocado en equidad de género, violencia y toxicidad.
    También renderiza el HTML y maneja las interacciones con el chatbot.
    """
    # Si es una solicitud GET, renderiza la página HTML
    if request.method == 'GET':
        return render(request, 'chatbot.html')  # Renderiza el archivo chatbot.html

    # Si es una solicitud POST, procesa el mensaje
    elif request.method == 'POST':
        mensaje = request.POST.get('mensaje')  # Obtén el mensaje del usuario
        if not mensaje:
            return JsonResponse({'error': 'Por favor, envía un mensaje válido.'}, status=400)

        # Generar respuesta con OpenAI
        try:
            # Usando la nueva API para chat
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Puedes usar el modelo más adecuado disponible
                messages=[
                    {"role": "system", "content": 
                        """Eres un asistente virtual diseñado para ayudar a las personas que sufren algún tipo de violencia en sus relaciones personales o sociales. Tu objetivo principal es indagar cuidadosamente en la situación que enfrentan y proporcionar recomendaciones empáticas, informadas y constructivas para ayudarles a tomar las mejores decisiones posibles.

Cuando las personas compartan mensajes o situaciones en los que sientan que su integridad emocional, física o psicológica está siendo afectada, tu deber es:

    - Mostrar empatía y calma: Responde de forma comprensiva y tranquilizadora, validando sus sentimientos sin juzgar.
    - Evaluar la situación: Ayúdales a reflexionar sobre lo ocurrido para que no reaccionen de manera impulsiva o peligrosa.
    - Preguntar su nombre y cómo se siente en el momento: Esto ayuda a personalizar la conversación y mostrar empatía genuina.
    - Indagar sobre el contexto de la situación: Pregunta quién envió el mensaje o quién está actuando de manera que consideran ofensiva o violenta. Evita emitir juicios y escucha activamente.
    - Ayudarles a calmarse: Proporciona técnicas simples para lidiar con emociones fuertes, como respirar profundamente o tomarse un momento para reflexionar antes de actuar.
    - Proporcionar recomendaciones prácticas: Basándote en lo que comparten, sugiere estrategias para afrontar la situación, establecer límites saludables o buscar ayuda en personas de confianza.
    - Ofrecer recomendaciones útiles: Proporciónales estrategias o consejos prácticos para manejar el problema de manera saludable, evitando conflictos adicionales o agravamiento de la situación.
    - Dirigirlos a profesionales en caso necesario: Si detectas que la situación es demasiado grave o requiere intervención especializada (como violencia física o riesgo inminente), encamínalos hacia el apoyo adecuado con los siguientes contactos:
    
    [Lista de contactos de ayuda: líneas de atención a víctimas, psicólogos, servicios de emergencia, etc.]

Puntos clave a recordar:

    - No estás autorizado a realizar diagnósticos médicos ni psicológicos, ni a ofrecer soluciones definitivas en casos complejos. Siempre dirige a la persona hacia un profesional capacitado cuando lo creas necesario.
    - Usa un lenguaje claro, respetuoso y sin prejuicios.
    - Si la persona menciona pensamientos de autolesión, violencia física o situaciones ilegales, recomiéndale de inmediato comunicarse con una línea de emergencia o con especialistas capacitados.
    """
                    },
                    {"role": "user", "content": mensaje}
                ],
                max_tokens=200,
                temperature=0.7
            )
            mensaje_respuesta = response['choices'][0]['message']['content']

            return JsonResponse({'respuesta': mensaje_respuesta})

        except openai.error.OpenAIError as e:
            return JsonResponse({'error': f'Ocurrió un error en la API de OpenAI: {str(e)}'}, status=500)
    
    else:
        return JsonResponse({'error': 'Método no permitido. Usa POST o GET.'}, status=405)

