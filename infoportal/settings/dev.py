from .common import *

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'infoportal',
        'USER': 'infoportal',
        'PASSWORD': 'infoportal',
        'HOST': 'localhost',
        'PORT': '',
    }
}

LOGGING['loggers']['integration'] = {
    'handlers': ['console_dev'],
    'level': 'DEBUG'
}
