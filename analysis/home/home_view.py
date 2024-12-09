from django.shortcuts import render

def home_views(request):
    # Código de la vista
    return render(request, 'index.html')
