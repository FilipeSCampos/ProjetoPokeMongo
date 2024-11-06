# pokemon_battle/settings.py

import mongoengine
from pathlib import Path

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurações de segurança
SECRET_KEY = 'sua-chave-secreta-aqui'
DEBUG = True
ALLOWED_HOSTS = []

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
        'DIRS': [],  # Adicione os diretórios de templates se necessário
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'pokemon_battle.wsgi.application'

# Banco de dados (usaremos MongoDB, então deixamos vazio aqui)
DATABASES = {}

# Configuração do MongoEngine
MONGODB_NAME = 'pokemon_battle_db'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

mongoengine.connect(
    db=MONGODB_NAME,
    host=MONGODB_HOST,
    port=MONGODB_PORT
)

# Autenticação personalizada usando MongoEngine (opcional)
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

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
