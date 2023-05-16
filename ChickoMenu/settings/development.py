from .base import *  # noqa

INSTALLED_APPS = INSTALLED_APPS + ["django_extensions"]
CORS_ALLOW_ALL_ORIGINS = True
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