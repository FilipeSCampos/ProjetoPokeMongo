# populate_db.py

import os
import django
from datetime import datetime
from uuid import uuid4

# Configuração do ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pokemon_battle.settings')
django.setup()

from game.models import Type, Attack, Pokemon, Battle, Score, Trainer
from game.utils import get_or_create  # Importar a função auxiliar
from django.contrib.auth.hashers import make_password

# Função para gerar UUID
def generate_uuid():
    return str(uuid4())

# Definição dos Tipos
tipos = {
    "Grass" : {"super_efetivo_contra":["Water", "Ground"], "pouco_efetivo_contra" : ["Fire"]},
    "Water" : {"super_efetivo_contra": ["Fire", "Rock", "Ice"], "pouco_efetivo_contra":["Grass"]},
    "Dark": {"super_efetivo_contra": ["Psychic", "Ghost"], "pouco_efetivo_contra": ["Fighting", "Dark", "Fairy"]},
    "Normal": {"super_efetivo_contra": [], "pouco_efetivo_contra": ["Rock", "Steel"]},
    "Poison": {"super_efetivo_contra": ["Grass", "Fairy"], "pouco_efetivo_contra": ["Poison", "Ground", "Rock", "Ghost"]},
    "Fire": {"super_efetivo_contra": ["Grass", "Ice", "Bug", "Steel"], "pouco_efetivo_contra": ["Fire", "Water", "Rock", "Dragon"]},
    "Fighting": {"super_efetivo_contra": ["Normal", "Ice", "Rock", "Dark", "Steel"], "pouco_efetivo_contra": ["Poison", "Flying", "Psychic", "Bug", "Fairy"]},
    "Fairy": {"super_efetivo_contra": ["Fighting", "Dragon", "Dark"], "pouco_efetivo_contra": ["Fire", "Poison", "Steel"]},
    "Ground": {"super_efetivo_contra": ["Fire", "Electric", "Poison", "Rock", "Steel"], "pouco_efetivo_contra": ["Grass", "Bug"]},
    "Electric": {"super_efetivo_contra": ["Water", "Flying"], "pouco_efetivo_contra": ["Electric", "Grass", "Dragon"]},
    "Ice": {"super_efetivo_contra": ["Grass", "Ground", "Flying", "Dragon"], "pouco_efetivo_contra": ["Fire", "Water", "Ice", "Steel"]},
    "Rock": {"super_efetivo_contra": ["Fire", "Ice", "Flying", "Bug"], "pouco_efetivo_contra": ["Fighting", "Ground", "Steel"]},
    "Dragon": {"super_efetivo_contra": ["Dragon"], "pouco_efetivo_contra": ["Steel"]},
    "Ghost": {"super_efetivo_contra": ["Psychic", "Ghost"], "pouco_efetivo_contra": ["Dark"]},
    "Psychic": {"super_efetivo_contra": ["Fighting", "Poison"], "pouco_efetivo_contra": ["Psychic", "Steel"]},
    "Steel": {"super_efetivo_contra": ["Ice", "Rock", "Fairy"], "pouco_efetivo_contra": ["Fire", "Water", "Electric", "Steel"]},
    # Adicione mais tipos conforme necessário
}

# Inserção dos Tipos
for tipo_nome, efetividades in tipos.items():
    tipo_obj, created = get_or_create(
        Type,
        tipo=tipo_nome,
        defaults={
            'super_efetivo_contra': efetividades['super_efetivo_contra'],
            'pouco_efetivo_contra': efetividades['pouco_efetivo_contra']
        }
    )
    if created:
        print(f'Tipo {tipo_nome} criado.')
    else:
        print(f'Tipo {tipo_nome} já existe.')

# Definição dos Ataques com danos base
ataques = [
    # Umbreon
    {"nome": "Last Resource", "tipo": "Normal", "dano_base": 50, "descricao": "Ataque normal de Umbreon."},
    {"nome": "Toxic", "tipo": "Poison", "dano_base": 0, "descricao": "Envenena o oponente."},
    {"nome": "Protect", "tipo": "Normal", "dano_base": 0, "descricao": "Protege de ataques próximos."},
    {"nome": "Bite", "tipo": "Dark", "dano_base": 60, "descricao": "Ataque de mordida escura."},

    # Infernape
    {"nome": "Nasty Plot", "tipo": "Dark", "dano_base": 0, "descricao": "Aumenta o ataque de Infernape."},
    {"nome": "Fire Blast", "tipo": "Fire", "dano_base": 110, "descricao": "Explosão de fogo poderosa."},
    {"nome": "Focus Blast", "tipo": "Fighting", "dano_base": 120, "descricao": "Focado ataque de luta."},
    {"nome": "Vacuum Wave", "tipo": "Fighting", "dano_base": 40, "descricao": "Ataque rápido de onda de luta."},

    # Clefable
    {"nome": "Moon Blast", "tipo": "Fairy", "dano_base": 95, "descricao": "Explosão lunar de fadas."},
    {"nome": "Soft-Boiled", "tipo": "Normal", "dano_base": 0, "descricao": "Recupera a saúde de Clefable."},
    {"nome": "Calm Mind", "tipo": "Psychic", "dano_base": 0, "descricao": "Aumenta a defesa mental."},
    {"nome": "Stealth Rock", "tipo": "Rock", "dano_base": 0, "descricao": "Cria pedras furtivas no campo."},

    # Kabutops
    {"nome": "Liquidation", "tipo": "Water", "dano_base": 85, "descricao": "Ataque de água poderoso."},
    {"nome": "Stone Edge", "tipo": "Rock", "dano_base": 100, "descricao": "Ataque de pedra afiada."},
    {"nome": "Knock Off", "tipo": "Dark", "dano_base": 65, "descricao": "Ataque que derruba itens do oponente."},
    {"nome": "Rapid Spin", "tipo": "Normal", "dano_base": 50, "descricao": "Ataque rápido de giro."},

    # Lucario
    {"nome": "Aura Sphere", "tipo": "Fighting", "dano_base": 80, "descricao": "Esfera de aura de luta."},
    {"nome": "Sword's Dance", "tipo": "Normal", "dano_base": 0, "descricao": "Dança da espada para aumentar o ataque."},
    {"nome": "Bullet Punch", "tipo": "Steel", "dano_base": 40, "descricao": "Soco de bala metálico."},
    {"nome": "Close Combat", "tipo": "Fighting", "dano_base": 120, "descricao": "Ataque de combate próximo."},

    # Ledian
    {"nome": "Power Up Punch", "tipo": "Fighting", "dano_base": 40, "descricao": "Soco de força."},
    {"nome": "Drain Punch", "tipo": "Fighting", "dano_base": 75, "descricao": "Soco drenante."},
    {"nome": "Ice Punch", "tipo": "Ice", "dano_base": 75, "descricao": "Soco de gelo."},
    {"nome": "Thunder Punch", "tipo": "Electric", "dano_base": 75, "descricao": "Soco elétrico."},

    # Snorlax
    {"nome": "Curse", "tipo": "Ghost", "dano_base": 0, "descricao": "Imputa maldição no oponente."},
    {"nome": "Body Slam", "tipo": "Normal", "dano_base": 85, "descricao": "Ataque corporal poderoso."},
    {"nome": "Rest", "tipo": "Psychic", "dano_base": 0, "descricao": "Snorlax descansa para recuperar HP."},
    {"nome": "Earthquake", "tipo": "Ground", "dano_base": 100, "descricao": "Ataque de terremoto."},

    # Shedinja
    {"nome": "Will-O-Wisp", "tipo": "Fire", "dano_base": 0, "descricao": "Imputa queimadura no oponente."},
    {"nome": "Protect", "tipo": "Normal", "dano_base": 0, "descricao": "Protege de ataques próximos."},
    {"nome": "Shadow Sneak", "tipo": "Ghost", "dano_base": 40, "descricao": "Ataque furtivo de sombra."},
    {"nome": "Toxic", "tipo": "Poison", "dano_base": 0, "descricao": "Envenena o oponente."},

    # Goodra
    {"nome": "Draco Meteor", "tipo": "Dragon", "dano_base": 130, "descricao": "Meteoros de dragão poderosos."},
    {"nome": "Dragon Claw", "tipo": "Dragon", "dano_base": 80, "descricao": "Garras de dragão afiadas."},
    {"nome": "Thunderbolt", "tipo": "Electric", "dano_base": 90, "descricao": "Raio elétrico poderoso."},
    {"nome": "Fire Blast", "tipo": "Fire", "dano_base": 110, "descricao": "Explosão de fogo intensa."},
]

# Inserção dos Ataques
for atk in ataques:
    tipo_nome = atk['tipo']
    tipo_obj, created = get_or_create(
        Type,
        tipo=tipo_nome,
        defaults={
            'super_efetivo_contra': tipos[tipo_nome]['super_efetivo_contra'],
            'pouco_efetivo_contra': tipos[tipo_nome]['pouco_efetivo_contra']
        }
    )
    if created:
        print(f'Tipo {tipo_nome} criado para o ataque {atk["nome"]}.')
    # Não é necessário printar se o tipo já existe para cada ataque

    # Agora, criar ou obter o ataque
    ataque_obj, created = get_or_create(
        Attack,
        nome=atk['nome'],
        defaults={
            'tipo': tipo_obj,
            'dano_base': atk['dano_base'],
            'descricao': atk['descricao']
        }
    )
    if created:
        print(f'Ataque {atk["nome"]} criado.')
    else:
        print(f'Ataque {atk["nome"]} já existe.')

# Definição dos Pokémons com seus ataques e status iniciais
pokemons = [
    {
        "nome": "Umbreon",
        "tipos": ["Dark"],
        "habilidades": ["Last Resource", "Toxic", "Protect", "Bite"],
        "status": {"HP": 100, "Ataque": 65, "Defesa": 60, "Velocidade": 65},
        "imagem_url": "game/images/umbreon.png"  # Caminho relativo à STATIC_ROOT
    },
    {
        "nome": "Infernape",
        "tipos": ["Fire", "Fighting"],
        "habilidades": ["Nasty Plot", "Fire Blast", "Focus Blast", "Vacuum Wave"],
        "status": {"HP": 106, "Ataque": 104, "Defesa": 71, "Velocidade": 108},
        "imagem_url": "game/images/infernape.png"
    },
    {
        "nome": "Clefable",
        "tipos": ["Fairy"],
        "habilidades": ["Moon Blast", "Soft-Boiled", "Calm Mind", "Stealth Rock"],
        "status": {"HP": 95, "Ataque": 70, "Defesa": 73, "Velocidade": 60},
        "imagem_url": "game/images/clefable.png"
    },
    {
        "nome": "Kabutops",
        "tipos": ["Rock", "Water"],
        "habilidades": ["Liquidation", "Stone Edge", "Knock Off", "Rapid Spin"],
        "status": {"HP": 60, "Ataque": 115, "Defesa": 105, "Velocidade": 80},
        "imagem_url": "game/images/kabutops.png"
    },
    {
        "nome": "Lucario",
        "tipos": ["Fighting", "Steel"],
        "habilidades": ["Aura Sphere", "Sword's Dance", "Bullet Punch", "Close Combat"],
        "status": {"HP": 70, "Ataque": 110, "Defesa": 70, "Velocidade": 90},
        "imagem_url": "game/images/lucario.png"
    },
    {
        "nome": "Ledian",
        "tipos": ["Bug", "Flying"],
        "habilidades": ["Power Up Punch", "Drain Punch", "Ice Punch", "Thunder Punch"],
        "status": {"HP": 55, "Ataque": 35, "Defesa": 50, "Velocidade": 85},
        "imagem_url": "game/images/ledian.png"
    },
    {
        "nome": "Snorlax",
        "tipos": ["Normal"],
        "habilidades": ["Curse", "Body Slam", "Rest", "Earthquake"],
        "status": {"HP": 160, "Ataque": 110, "Defesa": 65, "Velocidade": 30},
        "imagem_url": "game/images/snorlax.png"
    },
    {
        "nome": "Shedinja",
        "tipos": ["Ghost", "Bug"],
        "habilidades": ["Will-O-Wisp", "Protect", "Shadow Sneak", "Toxic"],
        "status": {"HP": 1, "Ataque": 90, "Defesa": 45, "Velocidade": 40},
        "imagem_url": "game/images/shedinja.png"
    },
    {
        "nome": "Goodra",
        "tipos": ["Dragon"],
        "habilidades": ["Draco Meteor", "Dragon Claw", "Thunderbolt", "Fire Blast"],
        "status": {"HP": 90, "Ataque": 100, "Defesa": 70, "Velocidade": 80},
        "imagem_url": "game/images/goodra.png"
    },
]

# Inserção dos Pokémons
for poke in pokemons:
    # Obter os tipos do Pokémon
    tipos_obj = Type.objects(tipo__in=poke['tipos'])
    # Obter os ataques do Pokémon
    ataques_obj = Attack.objects(nome__in=poke['habilidades'])

    # Criar ou obter o Pokémon
    pokemon_obj, created = get_or_create(
        Pokemon,
        nome=poke['nome'],
        defaults={
            'tipos': list(tipos_obj),
            'habilidades': poke['habilidades'],
            'status': poke['status'],
            'imagem_url': poke['imagem_url'],
            'ataques': list(ataques_obj),
            'dono': None  # Ajuste conforme necessário
        }
    )
    if created:
        print(f'Pokémon {poke["nome"]} criado.')
    else:
        print(f'Pokémon {poke["nome"]} já existe.')
