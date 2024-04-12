from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import show_comments
urlpatterns = [
    path('admin/', admin.site.urls),
    path('show/', show_comments, name='show_comments'),
]
