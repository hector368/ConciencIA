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
    Vista para manejar solicitudes al chatbot enfocado en equidad de género y toxicidad.
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
            # Usando la nueva API para chat (en lugar de Completion.create)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Puedes usar el modelo más adecuado disponible
                messages=[
                    {"role": "system", "content": "Eres un chatbot experto en temas de equidad de género y toxicidad."},
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
