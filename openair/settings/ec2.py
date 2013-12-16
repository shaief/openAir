from os import environ
from .base import *

ENV = 'ec2'

SECRET_KEY = environ.get('SECRET_KEY')
