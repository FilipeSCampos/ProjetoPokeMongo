# game/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from game.models import User, Battle, Pokemon, Attack, Type, Score
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from datetime import datetime
import uuid

# Função para calcular multiplicador de dano
def calcular_multiplicador(tipo_ataque, tipos_defensor):
    multiplicador = 1
    tipo_info = Type.objects(tipo=tipo_ataque.tipo).first()
    if not tipo_info:
        return multiplicador  # Tipo desconhecido, sem multiplicador
    for tipo in tipos_defensor:
        if tipo in tipo_info.super_efetivo_contra:
            multiplicador *= 2
        elif tipo in tipo_info.pouco_efetivo_contra:
            multiplicador *= 0.5
    return multiplicador

# Função para gerar UUID
def generate_uuid():
    return str(uuid.uuid4())

# View para Cadastro de Treinador
class RegisterView(APIView):
    def post(self, request):
        data = request.data
        nome_usuario = data.get('nome_usuario')
        email = data.get('email')
        senha = data.get('senha')

        if not nome_usuario or not email or not senha:
            return Response({"error": "Todos os campos são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects(nome_usuario=nome_usuario).first():
            return Response({"error": "Nome de usuário já existe."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects(email=email).first():
            return Response({"error": "Email já registrado."}, status=status.HTTP_400_BAD_REQUEST)

        user = User(
            nome_usuario=nome_usuario,
            email=email,
            email_verificado=False
        )
        user.set_password(senha)
        user.save()

        # Aqui você pode adicionar lógica para enviar um email de verificação

        return Response({"message": "Usuário registrado com sucesso."}, status=status.HTTP_201_CREATED)

# View para Autenticação de Treinador
class LoginView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        senha = data.get('senha')

        if not email or not senha:
            return Response({"error": "Email e senha são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects(email=email).first()
        if not user:
            return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(senha):
            return Response({"error": "Senha incorreta."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.email_verificado:
            return Response({"error": "Email não verificado."}, status=status.HTTP_400_BAD_REQUEST)

        # Atualizar último login
        user.ultimo_login = datetime.utcnow()
        user.save()

        # Aqui você pode gerar e retornar um token de autenticação

        return Response({"message": "Login bem-sucedido."}, status=status.HTTP_200_OK)

# View para Iniciar uma Batalha
class InitiateBattleView(APIView):
    def post(self, request):
        data = request.data
        treinador1_id = data.get('treinador1_id')
        treinador2_id = data.get('treinador2_id')  # Pode ser NPC ou outro usuário
        pokemon1_id = data.get('pokemon1_id')
        pokemon2_id = data.get('pokemon2_id')

        # Validação dos IDs
        treinador1 = User.objects(usuario_id=treinador1_id).first()
        if not treinador1:
            return Response({"error": "Treinador1 não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        treinador2 = User.objects(usuario_id=treinador2_id).first()
        if not treinador2:
            return Response({"error": "Treinador2 não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        pokemon1 = Pokemon.objects(pokemon_id=pokemon1_id).first()
        if not pokemon1:
            return Response({"error": "Pokémon1 não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        pokemon2 = Pokemon.objects(pokemon_id=pokemon2_id).first()
        if not pokemon2:
            return Response({"error": "Pokémon2 não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Criação da batalha
        batalha = Battle(
            batalha_id=generate_uuid(),
            treinador1=treinador1,
            treinador2=treinador2,
            pokemon1=pokemon1,
            pokemon2=pokemon2,
            estado_batalha="em andamento",
            data_batalha=datetime.utcnow()
        )
        batalha.save()

        return Response({"message": "Batalha iniciada.", "batalha_id": batalha.batalha_id}, status=status.HTTP_201_CREATED)

# View para Realizar Ataque durante a Batalha
class PerformAttackView(APIView):
    def post(self, request):
        data = request.data
        batalha_id = data.get('batalha_id')
        atacante_id = data.get('atacante_id')  # "treinador1" ou "treinador2"
        ataque_nome = data.get('ataque_nome')

        batalha = Battle.objects(batalha_id=batalha_id).first()
        if not batalha:
            return Response({"error": "Batalha não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        if batalha.estado_batalha != "em andamento":
            return Response({"error": "Batalha já concluída."}, status=status.HTTP_400_BAD_REQUEST)

        if atacante_id == 'treinador1':
            atacante = batalha.treinador1
            defensor = batalha.treinador2
            pokemon_atacante = batalha.pokemon1
            pokemon_defensor = batalha.pokemon2
        elif atacante_id == 'treinador2':
            atacante = batalha.treinador2
            defensor = batalha.treinador1
            pokemon_atacante = batalha.pokemon2
            pokemon_defensor = batalha.pokemon1
        else:
            return Response({"error": "Atacante inválido."}, status=status.HTTP_400_BAD_REQUEST)

        # Obter o ataque
        ataque = Attack.objects(nome=ataque_nome, tipo__in=pokemon_atacante.ataques).first()
        if not ataque:
            return Response({"error": "Ataque não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Verificar se o ataque é um buff de defesa
        if ataque.nome in ["Protect", "Soft-Boiled", "Calm Mind", "Stealth Rock", "Nasty Plot", "Will-O-Wisp", "Rest", "Sword's Dance"]:
            # Aplicar buff de defesa (aumentar HP em 20)
            pokemon_atacante.status['HP'] += 20
            pokemon_atacante.save()
            return Response({"message": f"{pokemon_atacante.nome} usou {ataque.nome} e aumentou seu HP em 20 pontos."}, status=status.HTTP_200_OK)

        # Calcular dano
        multiplicador = calcular_multiplicador(ataque, [tipo.tipo for tipo in pokemon_defensor.tipos])
        dano = ataque.dano_base * multiplicador

        # Aplicar dano ao defensor
        pokemon_defensor.status['HP'] -= dano
        if pokemon_defensor.status['HP'] < 0:
            pokemon_defensor.status['HP'] = 0
        pokemon_defensor.save()

        # Verificar se o defensor foi derrotado
        if pokemon_defensor.status['HP'] == 0:
            batalha.estado_batalha = "concluída"
            batalha.resultado = f"{atacante.nome_usuario} venceu."
            batalha.recompensas = {
                f"{atacante.nome_usuario}_pontos": 10,
                f"{defensor.nome_usuario}_pontos": 0
            }
            batalha.save()

            # Atualizar pontuação
            Score.objects.create(
                usuario=atacante,
                batalha=batalha,
                pontos=10
            )
            Score.objects.create(
                usuario=defensor,
                batalha=batalha,
                pontos=0
            )

            return Response({"message": f"{defensor.nome_usuario} foi derrotado. {atacante.nome_usuario} venceu!", "resultado": batalha.resultado}, status=status.HTTP_200_OK)

        batalha.save()

        return Response({"message": f"{pokemon_atacante.nome} usou {ataque.nome} e causou {dano} de dano.", "HP_defensor": pokemon_defensor.status['HP']}, status=status.HTTP_200_OK)

# View para Leaderboard
class LeaderboardView(APIView):
    def get(self, request):
        # Agregação para somar pontos por usuário
        pipeline = [
            {
                "$group": {
                    "_id": "$usuario_id",
                    "total_pontos": {"$sum": "$pontos"}
                }
            },
            {
                "$sort": {"total_pontos": -1}
            },
            {
                "$limit": 10  # Top 10
            }
        ]

        leaderboard = Score.objects.aggregate(*pipeline)
        leaderboard_list = []
        for entry in leaderboard:
            user = User.objects(usuario_id=entry['_id']).first()
            leaderboard_list.append({
                "nome_usuario": user.nome_usuario if user else "Desconhecido",
                "total_pontos": entry['total_pontos']
            })

        return Response({"leaderboard": leaderboard_list}, status=status.HTTP_200_OK)
