from django.db import models

class Record(models.Model):
    value = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField()

class Station(models.Model):
    name = models.CharField(max_length=25)
    lat = models.FloatField()
    lon = models.FloatField()
    active = models.BooleanField()
    url_id = models.PositiveIntegerField()

class Parameter(models.Model):
    abbr = models.CharField(max_length=10)
    name = models.CharField(max_length=25)
    name_hebrew = models.CharField(max_length=25)
    description = models.TextField()
    measurement_unit = models.CharField(max_length=25)
