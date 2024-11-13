# pokemongo/npc.py

import os
import django
from game.models import Trainer, Pokemon, Type, Attack
from game.utils import get_or_create

# Definir a variável de ambiente para o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pokemon_battle.settings')  # Ajuste o nome do módulo conforme necessário

# Inicializar o Django
django.setup()

def criar_npc():
    # Verificar se o NPC já existe para evitar duplicações
    npc = Trainer.objects(nome_usuario='NPC2').first()
    if npc:
        print("NPC2 já existe.")
    else:
        # Criar o Treinador NPC
        npc = Trainer(
            nome_usuario='NPC2',
            email='npc2@pokemon.com'
        )
        npc.set_password('npc2password')
        npc.save()
        print("NPC2 criado com sucesso.")

    # Criar Tipos utilizando a função get_or_create do utils.py
    electric = get_or_create(Type, tipo='Electric', defaults={
        'super_efetivo_contra': ['Water'],
        'pouco_efetivo_contra': ['Ground']
    })
    water = get_or_create(Type, tipo='Water', defaults={
        'super_efetivo_contra': ['Fire'],
        'pouco_efetivo_contra': ['Grass']
    })
    fire = get_or_create(Type, tipo='Fire', defaults={
        'super_efetivo_contra': ['Grass'],
        'pouco_efetivo_contra': ['Water']
    })
    grass = get_or_create(Type, tipo='Grass', defaults={
        'super_efetivo_contra': ['Water'],
        'pouco_efetivo_contra': ['Fire']
    })
    poison = get_or_create(Type, tipo='Poison', defaults={
        'super_efetivo_contra': ['Grass'],
        'pouco_efetivo_contra': ['Ground']
    })

    # Criar Ataques utilizando a função get_or_create do utils.py
    thunderbolt = get_or_create(Attack, nome='Thunderbolt', defaults={
        'tipo': electric,
        'dano_base': 40,
        'descricao': 'Ataque elétrico poderoso.'
    })
    hydro_pump = get_or_create(Attack, nome='Hydro Pump', defaults={
        'tipo': water,
        'dano_base': 50,
        'descricao': 'Ataque de água devastador.'
    })
    flame_thrower = get_or_create(Attack, nome='Flame Thrower', defaults={
        'tipo': fire,
        'dano_base': 45,
        'descricao': 'Lança chamas intensas.'
    })
    razor_leaf = get_or_create(Attack, nome='Razor Leaf', defaults={
        'tipo': grass,
        'dano_base': 35,
        'descricao': 'Folhas afiadas que cortam o inimigo.'
    })

    # Criar Pokémons para o NPC utilizando a função get_or_create do utils.py
    pikachu = get_or_create(Pokemon, nome='Pikachu', defaults={
        'tipos': [electric],
        'habilidades': ['Static'],
        'status': {'HP': 100, 'Attack': 55, 'Defense': 40},
        'imagem_url': r'pokemongo\game\static\game\images\pikachu.png',  # Use caminhos relativos com barras
        'ataques': [thunderbolt],
        'dono': npc  # Certifique-se de que o campo 'dono' existe no modelo Pokemon
    })
    bulbasaur = get_or_create(Pokemon, nome='Bulbasaur', defaults={
        'tipos': [grass, poison],
        'habilidades': ['Overgrow'],
        'status': {'HP': 100, 'Attack': 49, 'Defense': 49},
        'imagem_url': r'pokemongo\game\static\game\images\bulbasaur.png',
        'ataques': [razor_leaf],
        'dono': npc
    })
    charmander = get_or_create(Pokemon, nome='Charmander', defaults={
        'tipos': [fire],
        'habilidades': ['Blaze'],
        'status': {'HP': 100, 'Attack': 52, 'Defense': 43},
        'imagem_url': r'pokemongo\game\static\game\images\charmander.png',
        'ataques': [flame_thrower],
        'dono': npc
    })
    squirtle = get_or_create(Pokemon, nome='Squirtle', defaults={
        'tipos': [water],
        'habilidades': ['Torrent'],
        'status': {'HP': 100, 'Attack': 48, 'Defense': 65},
        'imagem_url': r'pokemongo\game\static\game\images\squirtle.png',
        'ataques': [hydro_pump],
        'dono': npc
    })

    print("Pokémons do NPC criados com sucesso.")

if __name__ == "__main__":
    criar_npc()
