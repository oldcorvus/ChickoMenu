from .base import *  # noqa

INSTALLED_APPS = INSTALLED_APPS + ["django_extensions"]
CORS_ALLOW_ALL_ORIGINS = True
SANDBOX = True
ZARINPAL_MERCHANT_ID = ''
DATABASES = {
"default": {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": "postgres",
    "USER": "postgres",
    "PASSWORD": "postgres",
    "HOST": "db",
    "PORT": 5432,
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}