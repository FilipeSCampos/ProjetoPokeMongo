# game/views.py

from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .serializers import TrainerSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Type, Attack, Pokemon, Battle, Score, Trainer
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from .utils import get_available_attacks, realizar_ataque, atualizar_leaderboard
from uuid import uuid4
from django.conf import settings
import datetime

# Função para gerar UUID
def generate_uuid():
    return str(uuid4())

# Função para gerar token JWT
def generate_jwt_token(trainer):
    import jwt
    from datetime import datetime, timedelta

    payload = {
        'id': str(trainer.id),
        'nome_usuario': trainer.nome_usuario,
        'exp': datetime.utcnow() + timedelta(hours=24),  # Token expira em 24 horas
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

# Decorator para requerer autenticação JWT
def jwt_required(view_func):
    from rest_framework.decorators import permission_classes
    from rest_framework.permissions import IsAuthenticated

    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            messages.error(request, "Cabeçalho de autorização ausente.")
            return redirect('login_page')
        try:
            token = auth_header.split(' ')[1]
            import jwt
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            trainer = Trainer.objects(id=payload['id']).first()
            if not trainer:
                messages.error(request, "Token inválido.")
                return redirect('login_page')
            request.trainer = trainer
        except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            messages.error(request, "Token inválido ou expirado.")
            return redirect('login_page')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# View para Cadastro de Treinador
class RegisterPageView(View):
    def get(self, request):
        return render(request, 'game/register.html')

    def post(self, request):
        nome_usuario = request.POST.get('nome_usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha2 = request.POST.get('senha2')

        if senha != senha2:
            messages.error(request, "As senhas não correspondem.")
            return redirect('register_page')

        # Verificar se o nome de usuário ou email já existe
        if Trainer.objects(nome_usuario=nome_usuario).first():
            messages.error(request, "Nome de usuário já existe.")
            return redirect('register_page')
        if Trainer.objects(email=email).first():
            messages.error(request, "Email já registrado.")
            return redirect('register_page')

        # Criar o treinador
        trainer = Trainer(
            nome_usuario=nome_usuario,
            email=email
        )
        trainer.set_password(senha)
        trainer.save()

        # Gerar token JWT
        token = generate_jwt_token(trainer)

        # Autenticar e logar o usuário
        user = authenticate(request, email=email, password=senha)
        if user is not None:
            login(request, user)
            request.session['jwt_token'] = token  # Armazena o token na sessão
            return redirect('battle_page')
        else:
            messages.error(request, "Erro ao autenticar usuário.")
            return redirect('register_page')

# View para Login de Treinador
class LoginPageView(View):
    def get(self, request):
        return render(request, 'game/login.html')

    def post(self, request):
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        trainer = authenticate(request, email=email, password=senha)
        if trainer is not None:
            login(request, trainer)
            # Gerar token JWT
            token = generate_jwt_token(trainer)
            request.session['jwt_token'] = token  # Armazena o token na sessão
            return redirect('battle_page')
        else:
            messages.error(request, "Credenciais inválidas.")
            return redirect('login_page')

# View para Logout
class LogoutView(View):
    def get(self, request):
        logout(request)
        request.session.flush()  # Limpa a sessão
        return redirect('login_page')

# View para Renderizar a Página de Batalha (Seleção de Pokémons)
class BattlePageView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login_page')
        # Obter Pokémons do Treinador
        pokemons = Pokemon.objects(dono=request.user)
        return render(request, 'game/battle.html', {'pokemons': pokemons})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login_page')
        # Obter IDs dos Pokémons selecionados
        pokemon_ids = request.POST.getlist('pokemon_ids')
        if len(pokemon_ids) != 3:
            messages.error(request, "Selecione exatamente 3 Pokémons para a batalha.")
            return redirect('battle_page')
        
        # Obter Pokémons do jogador
        pokemons = Pokemon.objects(id__in=pokemon_ids, dono=request.user)
        if pokemons.count() != 3:
            messages.error(request, "Pokémons inválidos selecionados.")
            return redirect('battle_page')
        
        # Selecionar 3 Pokémons aleatórios para o NPC
        npc = Trainer.objects(nome_usuario='NPC').first()
        if not npc:
            messages.error(request, "Treinador NPC não encontrado.")
            return redirect('battle_page')
        
        npc_pokemons = list(Pokemon.objects(dono=npc).order_by('?')[:3])
        if len(npc_pokemons) < 3:
            messages.error(request, "O NPC não possui Pokémons suficientes.")
            return redirect('battle_page')
        
        # Criar a batalha
        batalha = Battle(
            treinador1=request.user,
            treinador2=npc,
            pokemon1=pokemons[0],
            pokemon2=pokemons[1],
            pokemon3=pokemons[2],
            npc_pokemon1=npc_pokemons[0],
            npc_pokemon2=npc_pokemons[1],
            npc_pokemon3=npc_pokemons[2],
            estado_batalha="em andamento",
            data_batalha=datetime.utcnow(),
            logs=[]
        )
        batalha.save()

        # Armazenar o ID da batalha na sessão
        request.session['batalha_id'] = str(batalha.id)

        return redirect('perform_attack_page')

# View para Realizar Ataques na Batalha
class PerformAttackView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login_page')
        batalha_id = request.session.get('batalha_id')
        if not batalha_id:
            messages.error(request, "Nenhuma batalha em andamento.")
            return redirect('battle_page')
        
        try:
            batalha = Battle.objects.get(id=batalha_id)
        except Battle.DoesNotExist:
            messages.error(request, "Batalha não encontrada.")
            return redirect('battle_page')
        
        if batalha.estado_batalha != "em andamento":
            battle_result = batalha.resultado
            return render(request, 'game/perform_attack.html', {
                'battle_result': battle_result
            })
        
        player_pokemons = [batalha.pokemon1, batalha.pokemon2, batalha.pokemon3]
        npc_pokemons = [batalha.npc_pokemon1, batalha.npc_pokemon2, batalha.npc_pokemon3]
        available_attacks = get_available_attacks(player_pokemons)
        battle_logs = batalha.logs
        battle_result = batalha.resultado

        return render(request, 'game/perform_attack.html', {
            'player_pokemons': player_pokemons,
            'npc_pokemons': npc_pokemons,
            'available_attacks': available_attacks,
            'battle_logs': battle_logs,
            'battle_result': battle_result
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login_page')
        batalha_id = request.session.get('batalha_id')
        if not batalha_id:
            messages.error(request, "Nenhuma batalha em andamento.")
            return redirect('battle_page')
        
        ataque_nome = request.POST.get('ataque_nome')
        if not ataque_nome:
            messages.error(request, "Selecione um ataque.")
            return redirect('perform_attack_page')
        
        try:
            batalha = Battle.objects.get(id=batalha_id)
        except Battle.DoesNotExist:
            messages.error(request, "Batalha não encontrada.")
            return redirect('battle_page')
        
        if batalha.estado_batalha != "em andamento":
            messages.error(request, "A batalha já foi concluída.")
            return redirect('perform_attack_page')
        
        # Realizar o ataque
        logs = realizar_ataque(batalha, request.user, ataque_nome)

        return redirect('perform_attack_page')

# View para Leaderboard
class LeaderboardPageView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login_page')
        # Obter os scores ordenados, excluindo o NPC
        scores = Score.objects.order_by('-total_pontos')[:10]
        scores = [score for score in scores if score.usuario.nome_usuario != 'NPC']
        return render(request, 'game/leaderboard.html', {'leaderboard': scores})
