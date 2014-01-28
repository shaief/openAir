from unipath import FSPath as Path
import os

PROJECT_DIR = Path(__file__).absolute().ancestor(2)

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), ".."),
)


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

ALLOWED_HOSTS = []

TIME_ZONE = 'Asia/Jerusalem'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = '/webapps/static/'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    # PROJECT_DIR.child('static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#   'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'djangobower.finders.BowerFinder',
)

SECRET_KEY = 'supersecretkeythatisoverridedlateron'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'openair.urls'

WSGI_APPLICATION = 'openair.wsgi.application'

TEMPLATE_DIRS = (
    PROJECT_DIR.child('templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.gis',

    'django_extensions',
    'south',
    'tastypie',
    'django_nvd3',
    'djangobower',
    'gunicorn',

    'openair.records',
)


BOWER_COMPONENTS_ROOT = os.path.join(PROJECT_ROOT, 'components')

BOWER_INSTALLED_APPS = (
    'jquery#1.9',
    'underscore',
)

# on debian based systems 
# sudo  ln -s /usr/bin/nodejs /usr/bin/node

BOWER_PATH = "/usr/local/bin/bower"
SITE_ID = 1

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
