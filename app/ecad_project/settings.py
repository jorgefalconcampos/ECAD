"""
Django settings for ecad_project project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from decouple import config, Csv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_1&(a(w77hbg8h%!y33!(4tcn-yx67lhy6c%v(wrh9bbj@(56p'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = int(os.environ.get("DEBUG", default=0))


# ALLOWED_HOSTS = []
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", " ").split()


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ecad_app.apps.EcadAppConfig',
    'corsheaders',
    'crispy_forms',
    'taggit',
    'pwa',
    'django_summernote'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_WHITELIST = [
    'http://localhost:8000',
    'http://localhost:9000',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'
GOOGLE_RECAPTCHA_SECRET_KEY = os.environ.get("GOOGLE_RECAPTCHA_SECRET_KEY")

PWA_APP_NAME = 'ECAD' 
PWA_APP_START_URL = '/' 
PWA_APP_SCOPE = '/' 
PWA_APP_DISPLAY = 'standalone' 
PWA_APP_BACKGROUND_COLOR = '#EBEBEB' 
PWA_APP_THEME_COLOR = '#009CEE' 
PWA_APP_DESCRIPTION = "ECAD - PWA" 
PWA_APP_DIR = 'ltr' 
PWA_APP_LANG = 'en-US'
PWA_APP_ORIENTATION = 'portrait-primary' 
PWA_APP_STATUS_BAR_COLOR = 'default' 

PWA_APP_ICONS = [ { 'src': '/static/img/icons/r-icon.png', 'sizes': '160x160' }, { 'src': '/static/img/icons/r-icon-192.png', 'sizes': '192x192' },  { 'src': '/static/img/icons/r-icon-512.png', 'sizes': '512x512' } ] 
PWA_APP_ICONS_APPLE = [ { 'src': '/static/img/icons/r-icon.png', 'sizes': '160x160' } ] 
PWA_APP_SPLASH_SCREEN = [ { 'src': '/static/img/icons/splash-640x1136.png', 'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)' } ] 
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'ecad_app/static/js/pwa', 'serviceworker.js')

ROOT_URLCONF = 'ecad_project.urls'

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
                'django.template.context_processors.i18n',
                'ecad_app.ctxt_processors.searchPosts',
                'ecad_app.ctxt_processors.contactMsg',
                'ecad_app.ctxt_processors.newComment',
                'ecad_app.ctxt_processors.subscribeNewsletter',
                'ecad_app.ctxt_processors.newCategory',
            ],
        },
    },
]


WSGI_APPLICATION = 'ecad_project.wsgi.application'


# Email host server
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
DEFAULT_FROM_EMAIL = config('EMAIL_TO_ALIAS')
EMAIL_FROM = config('EMAIL_TO_ALIAS')
EMAIL_TO = config('EMAIL_TO_ALIAS')


CONTACT_HOST_USER = config('CONTACT_HOST_USER')
CONTACT_HOST_PASSWORD = config('CONTACT_HOST_PASSWORD')

NEWSLETTER_HOST_USER = config('NEWSLETTER_HOST_USER')
NEWSLETTER_HOST_PASSWORD = config('NEWSLETTER_HOST_PASSWORD')

USERS_HOST_USER = config('USERS_HOST_USER')
USERS_HOST_PASSWORD = config('USERS_HOST_PASSWORD')

#Configuración & opciones para el editor Summernote WYSIWYG Summernote
SUMMERNOTE_THEME = config('SUMMERNOTE_THEME')
X_FRAME_OPTIONS = config('X_FRAME_OPTIONS')

SUMMERNOTE_CONFIG = {
    'summernote': {
        'width': '99%',
        'height': '490',
    }
}


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        "ENGINE": os.environ.get("SQL_ENGINE"),
        "NAME": os.environ.get("SQL_DATABASE"),
        "USER": os.environ.get("SQL_USER"),
        "PASSWORD": os.environ.get("SQL_PASSWORD"),
        "HOST": os.environ.get("SQL_HOST"),
        "PORT": os.environ.get("SQL_PORT"),
        "CONN_MAX_AGE": 60 * 10, #10 minutes - This set the TTL (TimeToLive) database to 10 minutes, by default Django closses the conn after each query
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

from django.utils.translation import ugettext_lazy as _

LANGUAGE_CODE = 'es'

LANGUAGES = (
    ('es', _('Spanish')),
    ('en', _('English')),
)

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Media files (subidos por usuarios, admins, autores, etc)
MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
