import os
from .common import *

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1').split(',')

DEBUG = os.getenv('DJANGO_DEBUG', False)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME', 'infoportal'),
        'USER': os.getenv('DB_USER', 'infoportal'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'infoportal'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': '',
    }
}
