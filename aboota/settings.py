# """
# Django settings for jrindia project.

# Generated by 'django-admin startproject' using Django 2.2.13.

# For more information on this file, see
# https://docs.djangoproject.com/en/2.2/topics/settings/

# For the full list of settings and their values, see
# https://docs.djangoproject.com/en/2.2/ref/settings/
# """

import os
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'at%j%u*wv4&ahb_cir-3c8!@$nxy0g7_&m!&^sucme3-5=+hhj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# CACHES = {
#    'default': {
#       'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#       'LOCATION': 'jrindia_cache',
#       'TIMEOUT': '3000000',
#         'OPTIONS': {
#             'MAX_ENTRIES': 10000000
#         }
#    }
# }

APPEND_SLASH = True 

ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"
# ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'django.contrib.humanize',
    'corsheaders',
    'django.contrib.admindocs',
    'rest_framework',
    'django.contrib.flatpages',
    'django_celery_beat',
    'wallets',
    'users',
    'import_export',
    'widget_tweaks',
    'compressor',
    'ticket',

    'level',
    'markdown_deux',  # Required for Knowledgebase item formatting
    'bootstrapform', # Required for nicer formatting of forms with the default templates
    'allauth',
    "allauth.account",
    "allauth.socialaccount",
    'crispy_forms',
    'django_countries',
    'storages',
    "django_comments",
    "graphene_django",
    "markdownx",
    "taggit",
    "home",
    'maintenancemode',
    'kyc',
    'django_crontab'
]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'maintenancemode.middleware.MaintenanceModeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'aboota.urls'
ASGI_APPLICATION = "aboota.routing.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

_TEMPLATE_CONTEXT_PROCESSORS = [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.tz",

                'aboota.processor.universally_used_data'
            ]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates/oscar'),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": _TEMPLATE_CONTEXT_PROCESSORS,
            "debug": DEBUG,
            'libraries':{
            'sum_tags': 'templatetags.sum_tags',
            }
        }
    },
]

WSGI_APPLICATION = 'aboota.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db1.sqlite3'),
#     }
# }

import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default='postgres://dbmasteruser:pb2d80740f512c8cb41341e3291ed05b6b3d480a@ls-dff3f02526dec6fd6545926edd21f876ed074863.cz4lglmvud83.ap-south-1.rds.amazonaws.com:5432/postgres',
        conn_max_age=600)}

ATOMIC_REQUESTS = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        'PATH': location('whoosh_index'),
    },
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []

OSCAR_ALLOW_ANON_CHECKOUT = True


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
    ('ar', _('Araibic')),
)

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

import mimetypes
mimetypes.add_type("text/css", ".css", True)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
AWS_ACCESS_KEY_ID = 'AKIA2G5C7FQ6DCI3B5H5'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'ipaymaticsbucket'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_STATIC_LOCATION = 'static'

ADMIN_MEDIA_PREFIX = 'https://punchline-app.s3.amazonaws.com/static/admin/'

# STATIC_URL = '/static/'
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)

STATICFILES_STORAGE = 'aboota.storage_backends.StaticStorage'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = os.path.join(BASE_DIR, 'public/static')
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'compressor.finders.CompressorFinder'
]

AWS_PUBLIC_MEDIA_LOCATION = 'media/public'
DEFAULT_FILE_STORAGE = 'aboota.storage_backends.PublicMediaStorage'

AWS_PRIVATE_MEDIA_LOCATION = 'media/private'
PRIVATE_FILE_STORAGE = 'aboota.storage_backends.PrivateMediaStorage'

MEDIA_ROOT_URL = '.'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

SITE_ID = 1

AUTH_USER_MODEL = "users.User"

ACCOUNT_FORMS = {'signup': 'users.forms.SimpleSignupForm'}

ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_LOGOUT_REDIRECT_URL ="/accounts/login/"
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True

LOGIN_REDIRECT_URL = '/users/'

LOGIN_URL = "/accounts/login/"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'email-smtp.ap-south-1.amazonaws.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'AKIA2G5C7FQ6AXZPCO5P'
DEFAULT_FROM_EMAIL = 'no-reply@ipaymatics.com'
EMAIL_HOST_PASSWORD = 'BDeTwx2J2od4quHpOruu9QIYr1hhzx62mkFNNipLnFB4'
IMPORT_EXPORT_USE_TRANSACTIONS = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        # By default we set everything to admin,
        # then open endpoints on a case-by-case basis
        'rest_framework.permissions.IsAdminUser',
    ),
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
}

from datetime import timedelta

SIMPLE_JWT = {
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'ACCESS_TOKEN_LIFETIME': timedelta(days=800),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=800),
}

CORS_ORIGIN_ALLOW_ALL = True

FILE_UPLOAD_PERMISSIONS = 0o640

CRONJOBS = [
    ('22 0 * * *', 'scan', '>> /tmp/scheduled_job.log')
]

COMPRESS_DEBUG_TOGGLE = False
COMPRESS_CSS_COMPRESSOR = 'compressor.css.CssCompressor'
COMPRESS_JS_COMPRESSOR = 'compressor.js.JsCompressor'
COMPRESS_PRECOMPILERS = ()
COMPRESS_PARSER = 'compressor.parser.AutoSelectParser'
COMPRESS_ENABLED = False
COMPRESS_ROOT = '../..'
COMPRESS_URL = '/'

ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_UNIQUE_EMAIL = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
# ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True