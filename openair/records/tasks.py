#tasks.py
import logging

from celery import Celery
from celery.task import periodic_task
from datetime import timedelta
from os import environ
from openair.records.management.commands import run_scraper


REDIS_URL = environ.get('REDISTOGO_URL', 'redis://localhost')

celery = Celery('tasks', broker=REDIS_URL)


@periodic_task(run_every=timedelta(minutes=10))
def run_scraper_command():
    logging.info(run_scraper)
