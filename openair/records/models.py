from django.db import models


class Zone(models.Model):
    url_id = models.IntegerField()
    name = models.CharField(max_length=25)


    def __unicode__(self):  # Python 3: def __str__(self):
        return '{}'.format(self.url_id)


class Station(models.Model):
    zone = models.ForeignKey(Zone)
    name = models.CharField(max_length=25)
    url_id = models.PositiveIntegerField()


    def __unicode__(self):  # Python 3: def __str__(self):
        return '{}'.format(self.url_id)


class Parameter(models.Model):
    abbr = models.CharField(max_length=10)
    name = models.CharField(max_length=25)
    description = models.TextField()
    units = models.CharField(max_length=25)


    def __unicode__(self):  # Python 3: def __str__(self):
        return self.abbr


class Record(models.Model):
    parameter = models.ForeignKey(Parameter)
    station = models.ForeignKey(Station)
    value = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField()


    def __unicode__(self):  # Python 3: def __str__(self):
        return '{0}  {1}  {2}  {3}'.format(self.parameter.abbr,
                                           self.station.url_id,
                                           self.timestamp,
                                           self.value)
