from oppgavegenerator.settings_secret import *
"""
Django settings for oppgavegenerator project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

#if socket.gethostname() == '158.38.101.36':     # Edit this to your domain name or production server IP-address
#    DEBUG = TEMPLATE_DEBUG = False
#else:
#    DEBUG = TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', '158.38.101.36']  # Edit this to your domain name or production server IP-address


# Application definition

INSTALLED_APPS = (
    'oppgavegen',
    'django.contrib.admin',
    'django.contrib.auth',          # needed for registration
    'django.contrib.sites',         # needed for registration
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',      #todo:see if we need this for anything.
    'django.contrib.staticfiles',
    'bootstrap3',                   # django-bootstrap-3
    'registration',                 # django-registration-redux
    'gunicorn',                     # gunicorn (for unix deployment)
    'django_tables2',               # django-tables2
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'oppgavegenerator.urls'

WSGI_APPLICATION = 'oppgavegenerator.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = '/var/www/oppgavegenerator/collectstatic/' # Static files on production server. Edit this accordingly. Should not be the same as STATIC_URL
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)


#PATH_PROJECT = os.path.realpath(os.path.dirname(__file__))
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
TEMPLATE_LOADERS = ['django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader']
TEMPLATE_CONTEXT_PROCESSORS = ['django.core.context_processors.request',
                               'django.contrib.auth.context_processors.auth',]

#REGISTRATION SETTINGS
REGISTRATION_OPEN = True
ACCOUNT_ACTIVATION_DAYS = 7     # Amount of days a user has to activate their account
REGISTRATION_AUTO_LOGIN = True  # Auto-login after activation. True/False
SITE_ID = 1                     # Temporary solution for local production-environment (contrib.sites)

LOGIN_URL = '/user/login/'
LOGOUT_URL = '/user/logout/'
