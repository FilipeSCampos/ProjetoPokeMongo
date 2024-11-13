# game/models.py

import uuid
from mongoengine import (
    Document,
    StringField,
    EmailField,
    ReferenceField,
    IntField,
    ListField,
    DictField,
    ImageField,
    DateTimeField,
    CASCADE,
)
from datetime import datetime

# Modelo de Treinador
class Trainer(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    nome_usuario = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    senha = StringField(required=True)  # Senha hash
    data_cadastro = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'trainer'
    }

    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.senha = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.senha)

# Modelo de Tipo
class Type(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    tipo = StringField(required=True, unique=True)
    super_efetivo_contra = ListField(StringField())
    pouco_efetivo_contra = ListField(StringField())

    meta = {
        'collection': 'tipo'
    }

# Modelo de Ataque
class Attack(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = StringField(required=True, unique=True)
    tipo = ReferenceField(Type, required=True)
    dano_base = IntField(required=True)
    descricao = StringField()

    meta = {
        'collection': 'ataque'
    }

# Modelo de Pokémon
class Pokemon(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = StringField(required=True, unique=True)
    tipos = ListField(ReferenceField(Type))
    habilidades = ListField(StringField())
    status = DictField()  # Exemplo: {'HP': 100, 'Attack': 55, 'Defense': 40}
    imagem_url = StringField(required=True)  # Alterado para StringField para armazenar caminhos de arquivos
    ataques = ListField(ReferenceField(Attack))
    dono = ReferenceField(Trainer, reverse_delete_rule=CASCADE)  # Adicionado para relacionar com Trainer

    meta = {
        'collection': 'pokemon'
    }
# Modelo de Batalha
class Battle(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    treinador1 = ReferenceField(Trainer, required=True)
    treinador2 = ReferenceField(Trainer, required=True)  # Pode ser outro Treinador ou NPC
    pokemon1 = ReferenceField(Pokemon, required=True)
    pokemon2 = ReferenceField(Pokemon, required=True)
    pokemon3 = ReferenceField(Pokemon, required=True)
    npc_pokemon1 = ReferenceField(Pokemon, required=True)
    npc_pokemon2 = ReferenceField(Pokemon, required=True)
    npc_pokemon3 = ReferenceField(Pokemon, required=True)
    estado_batalha = StringField(default="em andamento")  # "em andamento" ou "concluída"
    data_batalha = DateTimeField(default=datetime.utcnow)
    resultado = StringField()  # "Treinador1 venceu", "NPC venceu", etc.
    logs = ListField(StringField())  # Logs da batalha

    meta = {
        'collection': 'battle'
    }

# Modelo de Score
class Score(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    usuario = ReferenceField(Trainer, required=True, unique=True)
    total_pontos = IntField(default=0)

    meta = {
        'collection': 'score'
    }
