from django.db import models

class Zone(models.Model):
    url_id = models.PositiveIntegerField()
    name = models.CharField(max_length=25)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.word

class Station(models.Model):
    zone = models.ForeignKey(Zone, related_name='stations')
    name = models.CharField(max_length=25)
    lat = models.FloatField()
    lon = models.FloatField()
    active = models.BooleanField()
    url_id = models.PositiveIntegerField()
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.word

class Parameter(models.Model):
    abbr = models.CharField(max_length=10)
    name = models.CharField(max_length=25)
    name_hebrew = models.CharField(max_length=25)
    description = models.TextField()
    measurement_unit = models.CharField(max_length=25)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.word

class Record(models.Model):
    parameter = models.ForeignKey(Parameter, related_name='records')
    station = models.ForeignKey(Station, related_name='records')
    value = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField()
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.word
