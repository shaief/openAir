import dj_database_url
import urlparse

from os import environ
from .base import *

from datetime import timedelta

ENV = 'dokku'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = (
    'openair.dokku.shaief.com',
)

SECRET_KEY = environ.get('SECRET_KEY')

# DATABASES = {
#     'default': dj_database_url.config()
# }

DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))}

redis_url = urlparse.urlparse(environ.get('REDIS_URL'))

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '{}:{}'.format(redis_url.hostname, redis_url.port),
        'OPTIONS': {
            'DB': 0,
            'PASSWORD': redis_url.password,
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        },
    },
}

STATICFILES_STORAGE = DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_QUERYSTRING_AUTH = False
AWS_PRELOAD_METADATA = True
AWS_IS_GZIPPED = True
AWS_S3_SECURE_URLS = False
AWS_HEADERS = {
    # 'Cache-Control': 'public, max-age=86400',
}
STATIC_URL = 'https://{}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)

RAVEN_CONFIG = {
    'dsn': environ.get('SENTRY_DSN'),
}

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)

CELERYBEAT_SCHEDULE = {
    'records': {
        'task': 'openair.records.tasks.scrape_data',
        'schedule': timedelta(minutes=10)
    }
}
