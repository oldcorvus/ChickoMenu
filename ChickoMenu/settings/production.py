from .base import *  # noqa

SECURE_SSL_REDIRECT = True
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
DEBUG = False
REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200'
]
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
MIDDLEWARE = MIDDLEWARE + [
    "monitus.middleware.FailedLoginMiddleware",
    "monitus.middleware.Error403EmailsMiddleware",
]

EMAIL_HOST = env("EMAIL_HOST", default='')
EMAIL_PORT = env("EMAIL_PORT",  default='')
EMAIL_HOST_USER = env("EMAIL_HOST_USER",  default='')
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD",  default='')
EMAIL_USE_TLS = True


ADMINS = [("m", "moelcrow@email.here")]  # CHANGE THIS WITH YOUR EMAIL