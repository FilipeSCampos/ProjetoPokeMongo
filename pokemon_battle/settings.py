# pokemon_battle/settings.py

from pathlib import Path
from decouple import config
import mongoengine
from pymongo.server_api import ServerApi
import os

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurações de segurança
SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

# Aplicativos instalados
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',       # Django REST Framework
    'game',                 # Aplicativo do jogo
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLs
ROOT_URLCONF = 'pokemon_battle.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'game', 'templates')],  # Diretórios de templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Necessário para request.user
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'pokemon_battle.wsgi.application'

# ASGI (Opcional, mas recomendado)
ASGI_APPLICATION = 'pokemon_battle.asgi.application'

# Banco de dados (usaremos MongoDB, então deixamos vazio aqui)
DATABASES = {}

# Configuração do MongoEngine para MongoDB Atlas usando variável de ambiente
MONGODB_URI = config('MONGODB_URI')

mongoengine.connect(
    host=MONGODB_URI,
    server_api=ServerApi('1')  # Especifica a versão da API do servidor
)

# Autenticação personalizada usando MongoEngine
AUTHENTICATION_BACKENDS = [
    'game.auth_backends.MongoEngineBackend',  # Backend personalizado
    'django.contrib.auth.backends.ModelBackend',  # Para admins do Django
]

# Senhas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # Adicione mais validadores conforme necessário
]

# Internacionalização
LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Arquivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'game', 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Usado em produção

# Configurações de arquivos de mídia
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configurações do Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    )
}
