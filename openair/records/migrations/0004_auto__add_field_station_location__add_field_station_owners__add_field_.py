# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Station.location'
        db.add_column(u'records_station', 'location',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Station.owners'
        db.add_column(u'records_station', 'owners',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Station.date_of_founding'
        db.add_column(u'records_station', 'date_of_founding',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Station.lon'
        db.add_column(u'records_station', 'lon',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Station.lat'
        db.add_column(u'records_station', 'lat',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Station.height'
        db.add_column(u'records_station', 'height',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Station.location'
        db.delete_column(u'records_station', 'location')

        # Deleting field 'Station.owners'
        db.delete_column(u'records_station', 'owners')

        # Deleting field 'Station.date_of_founding'
        db.delete_column(u'records_station', 'date_of_founding')

        # Deleting field 'Station.lon'
        db.delete_column(u'records_station', 'lon')

        # Deleting field 'Station.lat'
        db.delete_column(u'records_station', 'lat')

        # Deleting field 'Station.height'
        db.delete_column(u'records_station', 'height')


    models = {
        u'records.parameter': {
            'Meta': {'object_name': 'Parameter'},
            'abbr': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'records.record': {
            'Meta': {'object_name': 'Record'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['records.Parameter']"}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['records.Station']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'records.station': {
            'Meta': {'object_name': 'Station'},
            'date_of_founding': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'owners': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'url_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['records.Zone']"})
        },
        u'records.zone': {
            'Meta': {'object_name': 'Zone'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'url_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['records']