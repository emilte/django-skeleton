from .base_settings import * # star is neccessary

import django_heroku
import os

ENV = "HEROKU"

ALLOWED_HOSTS = ['*']

# For whitenoise, heroku
# Extra lookup directories for collectstatic to find static files
STATICFILES_DIRS = (
    BASE_DIR / 'staticroot',
)

# Values are set in heroku dashboard
SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = os.environ.get('DEBUG', False)


#  Add configuration for static files storage using whitenoise, heroku
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # whitenoise, heroku
]

MIDDLEWARE_CLASSES = [
    'whitenoise.middleware.WhiteNoiseMiddleware', # whitenoise, heroku
]

# Activate Django-Heroku.
django_heroku.settings(locals())
