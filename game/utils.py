# game/utils.py

import random
from .models import Battle, Trainer, Pokemon, Attack, Score, Type
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from mongoengine import NotUniqueError


# game/utils.py

from mongoengine import NotUniqueError

# game/utils.py

from mongoengine import NotUniqueError

def get_or_create(model, **kwargs):
    """
    Simula o método get_or_create do Django ORM para MongoEngine.

    Args:
        model: Classe do documento do MongoEngine.
        **kwargs: Campos para buscar ou criar o documento. Pode incluir 'defaults'.

    Returns:
        tuple: (Documento encontrado ou criado, True se criado, False se existente)
    """
    defaults = kwargs.pop('defaults', {})
    try:
        # Tenta obter o documento existente
        instance = model.objects(**kwargs).first()
        if instance:
            return instance, False
        else:
            # Tenta criar um novo documento com os defaults
            instance = model(**kwargs, **defaults)
            instance.save()
            return instance, True
    except NotUniqueError:
        # Em caso de erro de unicidade, obtém o documento existente
        instance = model.objects(**kwargs).first()
        return instance, False



def get_available_attacks(pokemons):
    """
    Retorna uma lista de ataques disponíveis dos Pokémons fornecidos.
    """
    ataques = []
    for pokemon in pokemons:
        if pokemon.ataques:
            ataques.extend(pokemon.ataques)
    return ataques

def calcular_multiplicador(ataque, tipos_defensor):
    """
    Calcula o multiplicador de dano baseado nos tipos do ataque e do defensor.
    
    Args:
        ataque: Instância de Attack.
        tipos_defensor: Lista de tipos do Pokémon defensor.
        
    Returns:
        float: Multiplicador de dano.
    """
    multiplicador = 1
    tipo_info = ataque.tipo.tipo  # String do tipo do ataque
    type_chart = {
        'Electric': {'Water': 2, 'Ground': 0},
        'Water': {'Fire': 2, 'Grass': 0.5},
        'Fire': {'Grass': 2, 'Water': 0.5},
        'Grass': {'Water': 2, 'Fire': 0.5},
        'Poison': {'Grass': 2, 'Ground': 0.5},
        # Adicione outros tipos conforme necessário
    }
    
    if tipo_info in type_chart:
        for def_tipo in tipos_defensor:
            if def_tipo in type_chart[tipo_info]:
                multiplicador *= type_chart[tipo_info][def_tipo]
    return multiplicador

def realizar_ataque(batalha, atacante, ataque_nome=None):
    """
    Processa o ataque realizado por um atacante (Treinador ou NPC).
    Atualiza o HP do defensor, registra logs e atualiza o estado da batalha.
    
    Args:
        batalha: Instância de Battle.
        atacante: Instância de Trainer que está atacando.
        ataque_nome: Nome do ataque escolhido (se atacante não for NPC).
        
    Returns:
        list: Logs atualizados da batalha.
    """
    if atacante.nome_usuario == 'NPC' and not ataque_nome:
        # Selecionar um ataque aleatório para o NPC
        ataques = get_available_attacks([batalha.npc_pokemon1, batalha.npc_pokemon2, batalha.npc_pokemon3])
        if not ataques:
            batalha.logs.append("NPC não possui ataques disponíveis.")
            batalha.save()
            return batalha.logs
        ataque = random.choice(ataques)
    else:
        # Ataque selecionado pelo jogador
        try:
            ataque = Attack.objects.get(nome=ataque_nome)
        except Attack.DoesNotExist:
            batalha.logs.append(f"Ataque {ataque_nome} não encontrado.")
            batalha.save()
            return batalha.logs
    
    # Determinar o defensor
    if atacante.nome_usuario != 'NPC':
        # Defensor é o NPC
        defender_pokemon = random.choice([batalha.npc_pokemon1, batalha.npc_pokemon2, batalha.npc_pokemon3])
    else:
        # Defensor é o jogador
        defender_pokemon = random.choice([batalha.pokemon1, batalha.pokemon2, batalha.pokemon3])
    
    if defender_pokemon.status['HP'] <= 0:
        batalha.logs.append(f"{defender_pokemon.nome} já foi derrotado.")
        batalha.save()
        return batalha.logs
    
    multiplicador = calcular_multiplicador(ataque, defender_pokemon.tipos)
    dano = ataque.dano_base * multiplicador
    defender_pokemon.status['HP'] -= dano
    if defender_pokemon.status['HP'] < 0:
        defender_pokemon.status['HP'] = 0
    batalha.logs.append(f"{atacante.nome_usuario} usou {ataque.nome} e causou {dano} de dano em {defender_pokemon.nome}.")
    
    if defender_pokemon.status['HP'] <= 0:
        batalha.logs.append(f"{defender_pokemon.nome} foi derrotado.")
        batalha.estado_batalha = "concluída"
        if atacante.nome_usuario == 'NPC':
            batalha.resultado = "NPC venceu a batalha!"
        else:
            batalha.resultado = f"{atacante.nome_usuario} venceu a batalha!"
        atualizar_leaderboard(batalha)
    
    batalha.save()
    return batalha.logs

def atualizar_leaderboard(batalha):
    """
    Atualiza a pontuação do vencedor na leaderboard após a conclusão da batalha.
    
    Args:
        batalha: Instância de Battle.
    """
    vencedor = None
    if batalha.resultado.startswith("NPC"):
        vencedor = None  # NPC não ganha pontos
    else:
        vencedor_nome = batalha.resultado.split(" venceu a batalha!")[0]
        try:
            vencedor = Trainer.objects.get(nome_usuario=vencedor_nome)
        except Trainer.DoesNotExist:
            vencedor = None
    
    if vencedor and vencedor.nome_usuario != 'NPC':
        # Atualizar pontuação do vencedor
        score, created = Score.objects.get_or_create(usuario=vencedor)
        score.total_pontos += 10  # Incrementa 10 pontos por vitória
        score.save()
