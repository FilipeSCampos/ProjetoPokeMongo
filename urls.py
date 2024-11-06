# pokemon_battle/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('game.urls')),  # Inclui as URLs do aplicativo 'game'
]



###############################################################################

# game/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('battle/initiate/', views.InitiateBattleView.as_view(), name='initiate_battle'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    # Adicione mais rotas conforme necessário
]
