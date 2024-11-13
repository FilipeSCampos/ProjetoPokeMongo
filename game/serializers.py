# game/serializers.py

from rest_framework import serializers
from .models import Trainer
from django.contrib.auth.hashers import make_password

class TrainerSerializer(serializers.Serializer):
    nome_usuario = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    senha = serializers.CharField(write_only=True, min_length=6)

    def validate_nome_usuario(self, value):
        if Trainer.objects(nome_usuario=value).first():
            raise serializers.ValidationError("Nome de usuário já existe.")
        return value

    def validate_email(self, value):
        if Trainer.objects(email=value).first():
            raise serializers.ValidationError("Email já registrado.")
        return value

    def create(self, validated_data):
        trainer = Trainer(
            nome_usuario=validated_data['nome_usuario'],
            email=validated_data['email'],
            senha=make_password(validated_data['senha'])  # Hash da senha
        )
        trainer.save()
        return trainer
