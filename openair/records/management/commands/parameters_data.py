# coding=utf-8

import os
import csv

from django.core.management.base import BaseCommand

from openair.settings.base import PROJECT_DIR
from openair.records.models import Parameter

BASE_DIR = PROJECT_DIR


class Command(BaseCommand):
    help = 'Run it to fill the DB with parameters information' \
           'from "parameters.csv"'

    def handle(self, *args, **options):
        path = os.path.join(BASE_DIR,
                            'information',
                            'parameters.csv')
        with open(path) as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                if reader.line_num != 1:  # skip first row
                    try:
                        sh = int(row[4])
                    except ValueError:
                        sh = None
                    try:
                        s8h = int(row[5])
                    except ValueError:
                        s8h = None
                    try:
                        sd = int(row[6])
                    except ValueError:
                        sd = None
                    try:
                        sy = int(row[7])
                    except ValueError:
                        sy = None

                    try:
                        p = Parameter.objects.get(abbr=row[0])
                        p.name = row[1]
                        p.description = row[2]
                        p.units = row[3]
                        p.standard_hourly = sh
                        p.standard_8hours = s8h
                        p.standard_daily = sd
                        p.standard_yearly = sy
                    except Parameter.DoesNotExist:
                        p = Parameter.objects.create(
                            abbr=row[0],
                            name=row[1],
                            description=row[2],
                            units=row[3],
                            standard_hourly=sh,
                            standard_8hours=s8h,
                            standard_daily=sd,
                            standard_yearly=sy,
                        )
                    print "updated field: " + p.abbr
                    p.save()
