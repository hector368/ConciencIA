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
