from os import environ

from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gpacalc',
        'USER' : environ['DB_USERNAME'],
        'PASSWORD' : environ['DB_PASSWORD'],
    }
}

DEBUG = True

TEMPLATE_DEBUG = True