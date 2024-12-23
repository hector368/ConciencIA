from django.shortcuts import render
from django.http import JsonResponse
from .utils import analyze_text  # Asegúrate de que esta función esté implementada y funcional
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def perspective_views(request):
    if request.method == 'GET':
        # Renderiza la página HTML
        return render(request, 'index.html')

    if request.method == 'POST':
        try:
            # Leer texto o archivo del request
            text = request.POST.get('text', '')
            file = request.FILES.get('file', None)

            if file:
                if file.name.endswith('.txt'):
                    try:
                        text = file.read().decode('utf-8')  # Leer y decodificar archivo .txt
                    except Exception as e:
                        return JsonResponse({'error': 'Failed to read the file', 'details': str(e)}, status=400)
                else:
                    return JsonResponse({'error': 'Only .txt files are supported'}, status=400)

            if not text:
                return JsonResponse({'error': 'No text provided'}, status=400)

            # Llamar a la función de análisis
            result = analyze_text(text)  # Llama a tu función que usa la API Perspective
            scores = result.get('attributeScores', {})

            # Extraer los puntajes relevantes
            response_data = {
                'insult': scores.get('INSULT', {}).get('summaryScore', {}).get('value', 0),
                'toxicity': scores.get('TOXICITY', {}).get('summaryScore', {}).get('value', 0),
                'threat': scores.get('THREAT', {}).get('summaryScore', {}).get('value', 0),
                'severe_toxicity': scores.get('SEVERE_TOXICITY', {}).get('summaryScore', {}).get('value', 0),
            }

            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Failed to analyze text', 'details': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def analyze_text_view(request):
    if request.method == "POST":
        try:
            # Obtener el texto enviado desde el cliente
            data = json.loads(request.body)
            text = data.get("text", "")

            # Validar que el texto no esté vacío
            if not text:
                return JsonResponse({"status": "error", "message": "No text provided"}, status=400)

            # Llamar a la función utilitaria para analizar el texto
            analysis_result = analyze_text(text)

            # Validar si la API de Perspective respondió correctamente
            if "error" in analysis_result:
                return JsonResponse(
                    {"status": "error", "message": analysis_result["error"], "details": analysis_result.get("details")},
                    status=500
                )

            # Extraer los puntajes relevantes
            scores = analysis_result.get("attributeScores", {})
            response_data = {
                "status": "success",
                "insult": scores.get("INSULT", {}).get("summaryScore", {}).get("value", 0),
                "toxicity": scores.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0),
                "threat": scores.get("THREAT", {}).get("summaryScore", {}).get("value", 0),
                "severe_toxicity": scores.get("SEVERE_TOXICITY", {}).get("summaryScore", {}).get("value", 0),
                "received_text": text,
            }

            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": "Unexpected error", "details": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

