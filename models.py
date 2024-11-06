# game/models.py

import uuid
from mongoengine import Document, StringField, IntField, ListField, ReferenceField, BooleanField, DateTimeField, DictField, EmbeddedDocument, EmbeddedDocumentField
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime

# Modelo de Usuário
class User(Document):
    usuario_id = StringField(required=True, unique=True, default=lambda: str(uuid.uuid4()))
    nome_usuario = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    senha_hash = StringField(required=True)
    data_cadastro = DateTimeField(default=datetime.utcnow)
    ultimo_login = DateTimeField()
    email_verificado = BooleanField(default=False)
    historico_batalhas = ListField(StringField())

    def set_password(self, raw_password):
        self.senha_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.senha_hash)

# Modelo de Tipo
class Type(Document):
    tipo = StringField(required=True, unique=True)  # Ex: "Água", "Fogo", etc.
    super_efetivo_contra = ListField(StringField())    # Tipos contra os quais é super efetivo
    pouco_efetivo_contra = ListField(StringField())   # Tipos contra os quais é pouco efetivo

# Modelo de Ataque
class Attack(Document):
    ataque_id = StringField(required=True, unique=True, default=lambda: str(uuid.uuid4()))
    nome = StringField(required=True)                 # Ex: "Fire Blast"
    tipo = ReferenceField(Type, required=True)        # Referência ao Tipo do Ataque
    dano_base = IntField(required=True)               # Dano base do ataque
    descricao = StringField()

# Modelo de Pokémon
class Pokemon(Document):
    pokemon_id = StringField(required=True, unique=True, default=lambda: str(uuid.uuid4()))
    nome = StringField(required=True)                 # Ex: "Infernape"
    tipos = ListField(ReferenceField(Type))           # Lista de Tipos do Pokémon
    nivel = IntField(default=1)
    habilidades = ListField(StringField())            # Ex: ["Fire Blast", "Focus Blast"]
    status = DictField()                              # Ex: {"HP": 100, "Ataque": 50, ...}
    imagem_url = StringField()                        # URL da imagem do Pokémon
    ataques = ListField(ReferenceField(Attack))       # Lista de Ataques disponíveis

# Modelo de Batalha
class Battle(Document):
    batalha_id = StringField(required=True, unique=True, default=lambda: str(uuid.uuid4()))
    treinador1 = ReferenceField(User, required=True)
    treinador2 = ReferenceField(User)  # Pode ser um NPC
    pokemon1 = ReferenceField(Pokemon, required=True)
    pokemon2 = ReferenceField(Pokemon, required=True)
    estado_batalha = StringField(default="em andamento")  # "em andamento", "concluída"
    resultado = StringField()                               # "treinador1 venceu", etc.
    data_batalha = DateTimeField(default=datetime.utcnow)
    recompensas = DictField()                               # Ex: {"treinador1_pontos": 10, "treinador2_pontos": 5}

# Modelo de Pontuação
class Score(Document):
    pontuacao_id = StringField(required=True, unique=True, default=lambda: str(uuid.uuid4()))
    usuario = ReferenceField(User, required=True)
    batalha = ReferenceField(Battle, required=True)
    pontos = IntField(required=True)
    data = DateTimeField(default=datetime.utcnow)
