"""
Django settings for transport project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$lpb&7dij%&@1-l%to3(jtocydhe9szr+i*)-apjbok!+zct)b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*','localhost', 'ot', 'cocointer.ci', 'cocointer']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]


INSTALLED_APPS += [
    #'widget_tweaks',
    'bootstrap4',
    'bootstrap_datepicker_plus',
    'crispy_forms',
    'mathfilters',
    
    'parametre',
    'carburant',
    'chauffeur',
    'vehicule',
    'marchandise',
    'commande',
    'detailscommande',
    'ordretransport',
    'enlevement',
    'facturation',
    'alerte',
    'entretien',
    'reparation',
    'planning',
    'reglement',
    'tableaubord',
    
    'devis',
    'client',
    'django_addanother',
]


CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'transport.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                ### PERMET DE FAIRE DES ALERTES DANS LES TEPLATES
                #'transport.context_processors.get_infos',
                'transport.context_processors.alerte_synthese', ### fonction placee a la racine
            ],
        },
    },
]

WSGI_APPLICATION = 'transport.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {    
    'default': {
        'ENGINE': 'django.db.backends.postgresql', #_psycopg2',
        'NAME': 'transportdb', #'
        'USER': 'postgres',
        'PASSWORD': 'azerty123',#admin?18',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

"""
# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Add this to tell Django where to redirect after
# successful login
LOGIN_REDIRECT_URL = 'parametre/accueil/'
# VARIABLE QUI PERMET UTILISER EXTENSION DE USER
AUTH_PROFILE_MODULE = "parametre.Profil"

CHEMIN_ETATS = os.path.join(BASE_DIR, 'etats\\')

print("directories = ", BASE_DIR)
print("CHEMIN_ETATS = ", CHEMIN_ETATS)

import glob
try:
    for filename in glob.glob(CHEMIN_ETATS+"*.*"):os.remove(filename)
except:pass

# DONNEES EXCEL A TRAITER
DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000 # higher than the count of fields


# POUR ENVOYER DES E-MAILS
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'kreadou@gmail.com'
EMAIL_HOST_USER = 'kreadou@gmail.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
#EMAIL_USE_SSL = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
