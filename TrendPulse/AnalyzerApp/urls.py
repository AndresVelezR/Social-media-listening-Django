from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .dash_apps.finished_apps import histogramdiagram, bardiagram, piediagram, hours, table1
from .views import clasification, submit_json_view, buttons_view, base, resultado_scraping, hacer_analisis, resultado_analisis, show_index, show_login, show_register, analysis, charts, comments_new
urlpatterns = [
    path('admin/', admin.site.urls),
    path('stats/', clasification , name='clasification'),
    path('', buttons_view, name='buttons'),  # Puedes mantener tus otras URLs aquí si las tienes
    path('submit_json/', submit_json_view, name='submit_json'),
    path('resultadoScraping/', resultado_scraping, name='resultado_scraping'),
    path('analisis/', hacer_analisis, name ='hacer_analisis'),
    path('resultadoAnalisis/', resultado_analisis, name = 'resultado_analisis'),
    path('index/', show_index, name = 'index'),
    path('login/', show_login, name = 'login'),
    path('register/', show_register, name = 'register'),
    #######################################################
    #######################################################
    path('analysis/', analysis, name='analysis'),
    path('charts/', charts, name='charts'),
    path('comments/', comments_new, name='comments'),
    path('base/', base, name='base'),
    path('the_django_plotly_dash/', include('django_plotly_dash.urls', namespace='the_django_plotly_dash')),
    
]
