#coding=utf-8
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = 'dev-only-insecure-key-firedeptmanagement-local-run'
ALLOWED_HOSTS = ['*']
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
MAPS_API_KEY = ''
GA = ''
BAJ_CONDITION = None
SUGGESTION_MAIL_SUBJECT = 'Nueva sugerencia'
SUGGESTION_MAIL_FROM = 'admin@admin.com'
SUGGESTION_MAIL_TO = ['admin@admin.com']

ADMINS = (
    ('admin', 'admin@admin.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_ROOT, 'sqlite.db'), # Or path to database file if using sqlite3.
        'USER': '', # Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '', # Or path to database file if using sqlite3.
        'USER': '', # Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}
TIME_ZONE = 'America/Caracas'
LANGUAGE_CODE = 'es-ve'

SITE_ID = 1
USE_I18N = True
USE_L10N = True

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'common',
    'personal',
    'capitalrelacional',
    'ops',
    'comunicaciones',
    #'opera',
    'sorl.thumbnail',
    'compat_bootstrap',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'common.context_processors.config_media',
            ],
        },
    },
]

MEDIA_ROOT = os.path.join(PROJECT_ROOT, '../media/')
MEDIA_URL = '/media/'

LOGIN_URL = "/login/"
LOGOUT_URL = "/logout/"

LOGIN_REDIRECT_URL = "/"

STATICFILES_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), './staticfiles/')
STATIC_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), './static/')
STATICFILES_URL = '/static/'
STATIC_URL = "/static/"

STATICFILES_DIRS = (
    STATICFILES_ROOT,
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_PROFILE_MODULE = "personal.Firefighter"
THUMBNAIL_DEBUG = True
DEFAULT_CHARSET = 'utf-8'

SITE_HEADER= u"<hgroup id='site_header'><h1>Cuerpo de Bomberos Voluntarios</h1><h2>UNIVERSIDAD SIMÓN BOLÍVAR</h2><h3>Disciplina - Estudio - Excelencia</h3></hgroup>"

LOGO_URL="img/logo_top.gif"

def send_webmaster_email(username):
    pass


def send_welcome_email(name, username, password, email):
    pass

try:
    from local_settings import *
except ImportError:
    pass
