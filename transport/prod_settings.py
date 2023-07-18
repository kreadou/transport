#import dj_database_url

from .settings import *

DEBUG = False

TEMPLATES_DEBUG = False

SECRET_KEY = 'lop&flwalww5y5t3x&=8sxuxl4mawg4s2zxybrw=xc1xj1gzo='

#DATABASES['default'] = dj_database_url.config()

ALLOWED_HOSTS = ['cocointer.herokuapp.com']

#MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

#STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
