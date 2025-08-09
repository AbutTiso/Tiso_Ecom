"""
Django settings for My_Ecom project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv()

# Security - NEVER hardcode in production!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-fallback-key-for-dev-only') 
DEBUG = os.getenv('DEBUG', 'False') == 'True'  # False in production

# Host settings
ALLOWED_HOSTS = [
    'tisoecom-production.up.railway.app',
    '.railway.app',  # Wildcard for all Railway subdomains
    '127.0.0.1',
    'localhost'
]
CSRF_TRUSTED_ORIGINS = ['https://tisoecom-production.up.railway.app']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'my_store',
    'cart',
    'payment',
    # Removed whitenoise.runserver_nostatic (not needed)
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Moved right after SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'My_Ecom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'My_Ecom.wsgi.application'

# Database - Using Railway's standard env vars
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PGDATABASE', 'railway'),
        'USER': os.getenv('PGUSER', 'postgres'),
        'PASSWORD': os.getenv('PGPASSWORD', os.getenv('DB_PASSWORD_YO', '')),
        'HOST': os.getenv('PGHOST', 'shinkansen.proxy.rlwy.net'),
        'PORT': os.getenv('PGPORT', '20498'),
    }
}

# Password validation (keep your existing validators)
AUTH_PASSWORD_VALIDATORS = [
    # ... (your existing validators remain unchanged) ...
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (corrected paths)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Changed to Path object
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Changed to Path object

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Production security (auto-enabled when DEBUG=False)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')