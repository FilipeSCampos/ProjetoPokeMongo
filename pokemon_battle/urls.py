# pokemon_battle/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('game.urls')),  # Inclui as URLs do aplicativo 'game'
]
