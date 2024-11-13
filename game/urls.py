# game/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('battles/', views.InitiateBattleView.as_view(), name='initiate_battle'),
    path('battles/attack/', views.PerformAttackView.as_view(), name='perform_attack'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    path('trainers/', views.TrainerListView.as_view(), name='trainer_list'),
    path('pokemons/', views.PokemonListView.as_view(), name='pokemon_list'),
    # Páginas Frontend
    path('register_page/', views.RegisterPageView.as_view(), name='register_page'),
    path('login_page/', views.LoginPageView.as_view(), name='login_page'),
    path('battle_page/', views.BattlePageView.as_view(), name='battle_page'),
    path('leaderboard_page/', views.LeaderboardPageView.as_view(), name='leaderboard_page'),
    path('logout/', views.LogoutView.as_view(), name='logout')
]
