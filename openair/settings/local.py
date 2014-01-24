from .base import *

ENV = 'local'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', $
            'NAME': 'openair',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': 'openair',
            'PASSWORD': 'tuuhrp,uj',
            'HOST': 'localhost',     # Empty for localhost through domain sockets or $
            'PORT': '',              # Set to empty string for default.
        }
    }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': PROJECT_DIR.child('db.sqlite3'),
#     }
# }

