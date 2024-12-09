"""
URL configuration for text_analysis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# text_analysis/urls.py
from django.contrib import admin
from django.urls import path, include
from analysis.perspective.perspective_view import perspective_views, analyze_text_view
from analysis.home.home_view import home_views
from analysis.chatbot.chatbot_view import chatbot_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views, name='home'),
    path('analysis/perspective/', perspective_views, name='perspective'),
    path('api/analyze/', analyze_text_view, name='analyze_text'),
    path('chatbot/', chatbot_view, name='chatbot'),
]
