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

# Application definition

INSTALLED_APPS = (
    'oppgavegen',
    #'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',
    'django.contrib.admin',         # django admin panel
    'django.contrib.auth',          # needed for registration
    'django.contrib.sites',         # needed for registration
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',                   # django-bootstrap-3
    'registration',                 # django-registration-redux
    'gunicorn',                     # gunicorn (for unix deployment)
    'haystack',
    'selectable'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
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

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

# Real-time indexing of new database objects. This might cause Whoosh! to crash under heavy load.
# http://django-haystack.readthedocs.org/en/v2.4.0/debugging.html#lockerror-errno-17-file-exists-path-to-whoosh-index-main-lock
# Consider using Solr-backend if problems occur (or use a queue-based signal processor)
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Oslo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# Static files on production server. Edit this accordingly. Should not be the same as STATIC_URL
STATIC_ROOT = '/var/www/oppgavegenerator/collectstatic/'
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

#PATH_PROJECT = os.path.realpath(os.path.dirname(__file__))
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
TEMPLATE_LOADERS = ['django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader']
TEMPLATE_CONTEXT_PROCESSORS = ['django.core.context_processors.request',
                               'django.contrib.auth.context_processors.auth',
                               'django.core.context_processors.debug']
#REGISTRATION SETTINGS
REGISTRATION_OPEN = True
ACCOUNT_ACTIVATION_DAYS = 7     # Amount of days a user has to activate their account
REGISTRATION_AUTO_LOGIN = True  # Auto-login after activation. True/False
REGISTRATION_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates/registration/")
SITE_ID = 1                     # Temporary solution for local production-environment (contrib.sites)

LOGIN_URL = '/user/login/'
LOGOUT_URL = '/user/logout/'
LOGIN_REDIRECT_URL = '/'
INCLUDE_REGISTER_URL = False

