# game/auth_backends.py

from django.contrib.auth.backends import BaseBackend
from .models import Trainer

class MongoEngineBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            trainer = Trainer.objects.get(email=email)
            if trainer.check_password(password):
                return trainer
        except Trainer.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Trainer.objects.get(id=user_id)
        except Trainer.DoesNotExist:
            return None
