import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

# Lógica de ALLOWED_HOSTS atualizada
ALLOWED_HOSTS = []

# Adiciona o host do Render se estiver em produção
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Adiciona o host do ngrok se estiver em desenvolvimento local com ngrok
NGROK_HOSTNAME = os.getenv('NGROK_HOSTNAME')
if NGROK_HOSTNAME:
    ALLOWED_HOSTS.append(NGROK_HOSTNAME)


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'accounts.apps.AccountsConfig',
    'spotify',
    'stats.apps.StatsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'spotify_stats.urls'

TEMPLATES = [ { 'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [], 'APP_DIRS': True, 'OPTIONS': { 'context_processors': [ 'django.template.context_processors.debug', 'django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages', ], }, }, ]
WSGI_APPLICATION = 'spotify_stats.wsgi.application'

if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
    }
else:
    DATABASES = { 'default': { 'ENGINE': 'django.db.backends.mysql', 'NAME': 'spotify_stats', 'USER': 'root', 'PASSWORD': 'maximo', 'HOST': 'localhost', 'PORT': '3306', 'OPTIONS': { 'init_command': "SET sql_mode='STRICT_TRANS_TABLES'" }, } }

AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STORAGES = { "staticfiles": { "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage", }, }

CORS_ALLOWED_ORIGINS = [
    os.getenv('FRONTEND_URL'),
    "https://melodious-pixie-ea3c85.netlify.app",
]

CSRF_TRUSTED_ORIGINS = []
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

REST_FRAMEWORK = { 'DEFAULT_AUTHENTICATION_CLASSES': [], 'DEFAULT_PERMISSION_CLASSES': [ 'rest_framework.permissions.AllowAny', ], }