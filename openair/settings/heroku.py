from os import environ
from .base import *

ENV = 'heroku'

SECRET_KEY = environ.get('SECRET_KEY')
