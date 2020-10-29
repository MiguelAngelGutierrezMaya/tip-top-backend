"""Development settings."""

from .base import *  # NOQA
from .base import env

# Base
DEBUG = True

# Security
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

# CORS
CORS_ORIGIN_WHITELIST = env.list('DJANGO_CORS_ORIGIN_WHITELIST')

# Static files
STATIC_ROOT = str(ROOT_DIR('/staticfiles'))

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# Templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # NOQA

# # Email
# EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025

# django-extensions
INSTALLED_APPS += ['django_extensions']  # noqa F405
