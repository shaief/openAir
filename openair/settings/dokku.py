from os import environ
from .base import *
import dj_database_url

ENV = 'dokku'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = environ.get('SECRET_KEY')

DATABASES = {
	'default': dj_database_url.config()
}