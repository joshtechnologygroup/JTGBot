# coding: utf-8
import environ

root = environ.Path(__file__) - 2
env = environ.Env(DEBUG=(bool, False), )
environ.Env.read_env(root('.env'))

# URL settings
APP_URL = env('APP_URL')
PORT = env('PORT', default=80)

# Sentry
RAVEN_CONFIG = {
    'dsn': env('RAVEN_DSN'),
}

# Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15
}
