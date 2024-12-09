import openai
from dotenv import load_dotenv
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from analysis.chatbot.utils import prompt_entrenamiento
import os

# Cargar las variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def chatbot_page(request):
    """
    Vista para renderizar la página del chatbot con un mensaje inicial (si se proporciona).
    """
    mensaje_inicial = request.GET.get('mensaje')  # Obtener el mensaje desde los parámetros GET
    respuesta_inicial = None

    if mensaje_inicial:
        # Hacer una llamada a OpenAI usando el mensaje inicial
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt_entrenamiento},
                    {"role": "user", "content": mensaje_inicial}
                ],
                max_tokens=200,
                temperature=0.7
            )
            respuesta_inicial = response['choices'][0]['message']['content']
        except openai.error.OpenAIError as e:
            respuesta_inicial = f"Error al procesar el mensaje inicial: {str(e)}"

    # Renderizar la plantilla con la respuesta inicial (si existe)
    return render(request, 'chatbot.html', {
        'mensaje_inicial': mensaje_inicial,
        'respuesta_inicial': respuesta_inicial
    })


def chatbot_request(request):
    """
    Vista para manejar solicitudes POST al chatbot.
    """
    if request.method == 'POST':
        mensaje = request.POST.get('mensaje')
        if not mensaje:
            return JsonResponse({'error': 'Por favor, envía un mensaje válido.'}, status=400)

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt_entrenamiento},
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
        return JsonResponse({'error': 'Método no permitido. Usa POST'}, status=405)
