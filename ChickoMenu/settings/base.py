import environ
from pathlib import Path
from django.utils.translation import gettext_lazy as _


BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env()
CELERY_BROKER_URL="redis://redis:6379"
CELERY_BACKEND="redis://redis:6379"

AUTH_USER_MODEL = "accounts.User"

SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", False)
API_KEY= env("API_KEY")





INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    #third party
    "rest_framework",
    'rest_framework.authtoken',
    'corsheaders',
    'djoser',
    'drf_yasg',

    #local
    "accounts.apps.AccountsConfig",
    "theme.apps.ThemeConfig",
    "menu.apps.MenuConfig",
    "plan.apps.PlanConfig",
    "payment.apps.PaymentConfig",


]




# DJOSER CONFIG
DJOSER = {
    "LOGIN_FIELD": "username",
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "SOCIAL_AUTH_TOKEN_STRATEGY": "djoser.social.token.jwt.TokenStrategy",
    "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": [
        "your redirect url",
        "your redirect url",
    ],
    "SERIALIZERS": {
        "user_create": "accounts.api.serializers.UserSerializer", # custom serializer
        "user": "accounts.api.serializers.UserSerializer",
        "current_user":"accounts.api.serializers.UserSerializer",
        "user_delete": "accounts.api.serializers.UserSerializer",
    },
}


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.locale.LocaleMiddleware', 
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]

import os 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = "ChickoMenu.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ChickoMenu.wsgi.application"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = 'fa'
TIME_ZONE = 'Asia/Tehran'

USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

LANGUAGES = [
    ('fa', _('Persian')),
    ('en', _('English')),
]

STATIC_URL = env("STATIC_URL")


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAdminUser"],
    'DEFAULT_THROTTLE_RATES': {
        "authentication": "8/hour",
        "verify_authentication": "8/hour",
    },

}