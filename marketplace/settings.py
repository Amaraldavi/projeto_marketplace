from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables using django-environ
import environ

# initialize environment
env = environ.Env(
    DEBUG=(bool, True),
)
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY', default='django-insecure-key')

DEBUG = env.bool('DEBUG', default=True)

# ALLOWED_HOSTS can be provided as a comma separated list in .env
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Render injeta o host público em RENDER_EXTERNAL_HOSTNAME — registramos cedo para
# que a checagem de ALLOWED_HOSTS em produção passe sem precisar setar à mão.
RENDER_EXTERNAL_HOSTNAME = env('RENDER_EXTERNAL_HOSTNAME', default=None)
if RENDER_EXTERNAL_HOSTNAME and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# =========================
# APPS
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Armazenamento de mídia na nuvem (Cloudinary)
    'cloudinary_storage',
    'cloudinary',

    # REMOVIDO: 'users'
    'marketplace_app',
]


# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise serve os arquivos estáticos em produção (logo após o SecurityMiddleware)
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'marketplace.urls'


# =========================
# TEMPLATES
# =========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'marketplace_app.context_processors.cart_counts',
                'marketplace_app.context_processors.notifications',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'marketplace.wsgi.application'


# =========================
# DATABASE
# =========================
# Em produção (Render/Railway/Heroku) usa-se DATABASE_URL. Localmente, caímos
# nas variáveis DB_* separadas. conn_max_age mantém conexões reutilizáveis.
if env('DATABASE_URL', default=None):
    DATABASES = {
        'default': env.db('DATABASE_URL'),
    }
    DATABASES['default']['CONN_MAX_AGE'] = env.int('DB_CONN_MAX_AGE', default=600)
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DB_NAME', default='marketplace_db'),
            'USER': env('DB_USER', default='postgres'),
            'PASSWORD': env('DB_PASSWORD', default='1234'),
            'HOST': env('DB_HOST', default='localhost'),
            'PORT': env('DB_PORT', default='5432'),
        }
    }


# =========================
# AUTH
# =========================
AUTH_USER_MODEL = 'marketplace_app.User'


# =========================
# PASSWORD
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# =========================
# INTERNATIONAL
# =========================
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True
USE_TZ = True


# =========================
# STATIC / MEDIA
# =========================
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Armazenamento (Django 5+). WhiteNoise comprime e versiona os estáticos em produção.
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# Mídia (imagens enviadas por usuários) no Cloudinary.
# O disco da Render é efêmero — sem isso, as imagens somem a cada deploy.
# Defina a variável de ambiente CLOUDINARY_URL na Render para ativar.
# Sem ela (ex.: ambiente local), cai no FileSystemStorage padrão acima.
CLOUDINARY_URL = env('CLOUDINARY_URL', default='')
if CLOUDINARY_URL:
    STORAGES['default'] = {
        'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
    }


# =========================
# EMAIL CONFIGURATION
# =========================
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')  # Para desenvolvimento - mostra emails no console
# SMTP example (configure .env for production)
# EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='')
EMAIL_PORT = env('EMAIL_PORT', default='')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=False)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='')

# External service tokens are configured in the PAYMENTS section below


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =========================
# PAYMENTS
# =========================
MERCADO_PAGO_ACCESS_TOKEN = env('MERCADO_PAGO_ACCESS_TOKEN', default='')
MERCADO_PAGO_PUBLIC_KEY = env('MERCADO_PAGO_PUBLIC_KEY', default='')
SITE_URL = env('SITE_URL', default='http://127.0.0.1:8000')


# =========================
# PRODUCTION HARDENING
# =========================
# Ensure SECRET_KEY is not the insecure default when running with DEBUG=False
if not DEBUG and SECRET_KEY == 'django-insecure-key':
    raise ImproperlyConfigured('SECRET_KEY must be set to a secure value in production')

# Cookie and SSL settings - default to secure when DEBUG is False
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=not DEBUG)
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=not DEBUG)
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=not DEBUG)

# HSTS - sensible defaults for production; can be overridden via .env
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=31536000 if not DEBUG else 0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
SECURE_HSTS_PRELOAD = env.bool('SECURE_HSTS_PRELOAD', default=True)

# When running behind a proxy/load-balancer that sets X-Forwarded-Proto
if env.bool('USE_X_FORWARDED_PROTO', default=False):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# X-Frame options
X_FRAME_OPTIONS = env('X_FRAME_OPTIONS', default='DENY')

# Enforce ALLOWED_HOSTS in production - keep empty for local development
if not DEBUG and not ALLOWED_HOSTS:
    raise ImproperlyConfigured('ALLOWED_HOSTS must be set in production')

# CSRF_TRUSTED_ORIGINS: domínios HTTPS confiáveis para POST/forms em produção.
# Defina no .env como lista separada por vírgula, ex.:
#   CSRF_TRUSTED_ORIGINS=https://meusite.com,https://www.meusite.com
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])

# Confia no host do Render para CSRF e ajusta o header de proxy HTTPS.
# (RENDER_EXTERNAL_HOSTNAME já foi adicionado a ALLOWED_HOSTS no topo do arquivo.)
if RENDER_EXTERNAL_HOSTNAME:
    origin = f'https://{RENDER_EXTERNAL_HOSTNAME}'
    if origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(origin)
    # Atrás do proxy do Render, o HTTPS chega via X-Forwarded-Proto
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')