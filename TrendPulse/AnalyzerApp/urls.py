from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import show_comments, clasification, show_chart, submit_json_view, index_view, resultado_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('show/', show_comments, name='show_comments'),
    path('stats/', clasification , name='clasification'),
    path('graph/', show_chart , name='graph'),
    path('', index_view, name='index'),  # Puedes mantener tus otras URLs aquí si las tienes
    path('submit_json/', submit_json_view, name='submit_json'),
    path('resultado/', resultado_view, name='resultado'),

    
]
