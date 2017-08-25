# coding: utf-8
import os

from conf.apps import *
from conf.etc import *

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

DEBUG = env.bool('DEBUG')
PRODUCTION = env.bool('PRODUCTION')

DATABASES = {'default': env.db()}

SITE_ID = 1

ADMINS = (
    ('Dmitry Astrikov', 'astrikov.d@gmail.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

TIME_ZONE = 'Asia/Krasnoyarsk'

LANGUAGE_CODE = 'ru'
LANGUAGES = (
    ('ru', 'Russian'),
)

USE_I18N = True

USE_L10N = True

USE_TZ = False
MEDIA_URL = '/data/'

STATIC_URL = '/static/'

STATICFILES_DIRS = ()

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
)

SECRET_KEY = env('SECRET_KEY')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

INSTALLED_APPS = (
                     'django.contrib.auth',
                     'django.contrib.admin',
                     'django.contrib.contenttypes',
                     'django.contrib.sessions',
                     'django.contrib.sites',
                     'django.contrib.messages',
                     'django.contrib.staticfiles',
                     'django.contrib.humanize',
                 ) + THIRD_PARTY_APPS + PROJECT_APPS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

DATE_INPUT_FORMATS = (
    '%d.%m.Y'
)

DATETIME_INPUT_FORMATS = (
    '%d.%m.Y %H:%M:%S'
)

ROOT_URLCONF = 'app.urls'
