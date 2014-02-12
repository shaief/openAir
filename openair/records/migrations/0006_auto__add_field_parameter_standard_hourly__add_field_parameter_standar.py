# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Parameter.standard_hourly'
        db.add_column(u'records_parameter', 'standard_hourly',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Parameter.standard_8hours'
        db.add_column(u'records_parameter', 'standard_8hours',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Parameter.standard_daily'
        db.add_column(u'records_parameter', 'standard_daily',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Parameter.standard_yearly'
        db.add_column(u'records_parameter', 'standard_yearly',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Parameter.standard_hourly'
        db.delete_column(u'records_parameter', 'standard_hourly')

        # Deleting field 'Parameter.standard_8hours'
        db.delete_column(u'records_parameter', 'standard_8hours')

        # Deleting field 'Parameter.standard_daily'
        db.delete_column(u'records_parameter', 'standard_daily')

        # Deleting field 'Parameter.standard_yearly'
        db.delete_column(u'records_parameter', 'standard_yearly')


    models = {
        u'records.parameter': {
            'Meta': {'object_name': 'Parameter'},
            'abbr': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'standard_8hours': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'standard_daily': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'standard_hourly': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'standard_yearly': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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