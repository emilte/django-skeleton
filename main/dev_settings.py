from .base_settings import *

ENV = "DEV" # Can be used in custom templatetags
print(f"Environment: {ENV}")

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DEBUG = True

SECRET_KEY = "NOT SET"

# Security
SECURE_HSTS_SECONDS = 0
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_BROWSER_XSS_FILTER = False
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
SECURE_HSTS_PRELOAD = False
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
CSRF_COOKIE_SECURE  = False
X_FRAME_OPTIONS = 'SAMEORIGIN'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
