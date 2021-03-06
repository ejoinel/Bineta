"""
Django settings for Bineta project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from tempfile import mkdtemp

DEFAULT_CHARSET = 'utf-8'
DEFAULT_CONTENT_TYPE = 'text/html'

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, 'templates'), )

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static'), )

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOCALE_PATHS = ('~/Projets/Perso/Bineta/Bineta/local',)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#WHOOSH_INDEX = os.path.join(BASE_DIR, 'whoosh/')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'va2#u=-e&z*&d2k)+4(z&_&*geyh$vr@l^z0*68i4fm%x6p+s&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

CRISPY_TEMPLATE_PACK = 'bootstrap3'

AUTH_USER_MODEL = 'Bineta.User'

# Passwords
PASSWORD_MIN_LENGTH = 6  # Defaults to 6
PASSWORD_MAX_LENGTH = 20  # Defaults to None

if DEBUG:
    # Email conf
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = 'ejoinel@gmail.com'
    SERVER_EMAIL = 'ejoinel@gmail.com'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'ejoinel@gmail.com'
    EMAIL_HOST_PASSWORD = '2NOUS_pau'
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.core.context_processors.media',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CSRF_FAILURE_VIEW = 'Bineta.views.csrf_failure'

# Application definition

DJANGO_APPS = (
    # django app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)



THIRD_PARTY_APPS = (
    # third party apps
    'crispy_forms',
    'passwords',
    'multiupload',
    'bootstrap_pagination',
    'rest_framework'
)



LOCAL_APPS = (
    # My app
    'Bineta',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'Bineta.urls'

WSGI_APPLICATION = 'Bineta.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sikolo',
        'USER': 'root',
        'PASSWORD': 'nous_pau',
        'HOST': 'localhost',  # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

gettext = lambda x: x

LANGUAGES = (('fr', gettext('French')), ('en', gettext('English')),)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
