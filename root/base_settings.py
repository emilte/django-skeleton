import os
from django.utils.encoding import force_bytes # QUESTION: fjerne?

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


"""
Base settings has all configurations that are used by the project in general.
It is also setup with strict configurations suitable for development.

Production server must:
1. Create its own settings file eg. prod_settings
2. from root.base_settings import *
3. Set SECRET_KEY
4. Set ENV
5. Configure DATABASES
6. Specify settings to use
"""

# Environments:
# useful in eg. templates
# override env in current settings (should not stay in BASE)
BASE = "BASE"
DEV = "DEV"
PROD = "PROD"
ENV = BASE

# Custom User model
# from django.contrib.auth import get_user_model; User = get_user_model()
AUTH_USER_MODEL = "accounts.User"

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'start3:nbb:dashboard' # TODO Update when full merge
LOGOUT_REDIRECT_URL = 'accounts:login'

DEBUG = False

ALLOWED_HOSTS = ['nbb.samfundet.no']


# The header which ITK ACL sets with a username when user is authenticated &
# authorized to access the given page
ACL_REMOTE_USER_HEADER = 'HTTP_REMOTE_USER'
ACL_EMAIL_SUFFIX = 'AD.SAMFUNDET.NO'
SAMFUNDET_EMAIL_SUFFIX = 'samfundet.no'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticroot')
STATIC_URL = '/static/'


# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE  = True
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_NAME = 'sessionid'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 24*60*60*7
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Application definition

PROJECT_APPS = [
    # main apps
    'accounts',
    'root',
    
    # start3
    'start3.adminpage',
    'start3.barvakt',
    'start3.main',
    'start3.nbb',
    'start3.privacypolicy',
]

INSTALLED_APPS = PROJECT_APPS + [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # QUESTION: brukes denne?
    # 'raven.contrib.django.raven_compat', # logging to sentry.io
    
    # imported apps
    'django_seed',
    'django_select2', # TESTING
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
   # 'django.contrib.auth.middleware.RemoteUserMiddleware',
    'start3.nbb.pipeline.remoteauth.CustomRemoteUserMiddleware', # replaces RemoteUserMiddleware
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'root.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'root.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'nb'
TIME_ZONE = 'Europe/Oslo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

AUTHENTICATION_BACKENDS = {
    'accounts.authentication.EmailOrUsernameModelBackend'
}

################## LOGGING ##################

import logging.config

LOGFILENAME = f"{BASE_DIR}/nbb.log"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': LOGFILENAME,
        },
    },
    'loggers': {
        'root': {
            'level': 'INFO',
            'handlers': ['file'],
        },
        'django': {
            'level': 'INFO',
            'handlers': ['file'],
            'propagate': True,
        },
    },
}

logging.config.dictConfig(LOGGING)

# from django.utils.log import DEFAULT_LOGGING
# import logging
# import logging.config
# logger = logging.getLogger(__name__)
#
#
# LOGGING_CONFIG = None
# LOGLEVEL = os.environ.get('DJANGO_LOGLEVEL', 'info').upper()
#
# START3_LOG_CONFIG = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'console': {
#             'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#         },
#         'django.server': DEFAULT_LOGGING['formatters']['django.server'],
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'console',
#         },
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': f'{BASE_DIR}/../nbb.log',
#         },
#         'django.server': DEFAULT_LOGGING['handlers']['django.server'],
#     },
#     'loggers': {
#         '': {
#             'level': 'INFO',
#             'handlers': ['console', 'file'],
#
#         },
#         'nbb': {
#             'level': LOGLEVEL,
#             'handlers': ['console'],
#             # required to avoid double logging with root logger
#             'propagate': False,
#         },
#         'django.server': DEFAULT_LOGGING['loggers']['django.server'],
#     },
# }
#
# # in case local_settings override log config.
# logging.config.dictConfig(START3_LOG_CONFIG)

################## END: LOGGING ##################


# Quick fix for avoiding concurrency issues related to db access
# Note: this might not be an ideal solution. See these links for information
# https://docs.djangoproject.com/en/1.10/topics/db/transactions/#django.db.transaction.on_commit
# https://medium.com/@hakibenita/how-to-manage-concurrency-in-django-models-b240fed4ee2
ATOMIC_REQUESTS = True
APPEND_SLASH = True

checklist = {
    # 'DEBUG': DEBUG,
    # 'DATABASES': DATABASES,
}

def check_settings(settings=None):
    print("|\n== CHECK SETTINGS ==")
    for k, v in settings.items():
        print("{} = {}".format(k, v))
    print('|')

# check_settings(checklist)

