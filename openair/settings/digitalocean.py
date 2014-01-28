from os import environ
from .base import *
import dj_databse_url

ENV = 'digitalocean'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = environ.get('SECRET_KEY')

DATABASES = {
	'default': dj_databse_url.config()
}