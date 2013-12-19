# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Parameter.name_hebrew'
        db.delete_column(u'records_parameter', 'name_hebrew')

        # Deleting field 'Parameter.measurement_unit'
        db.delete_column(u'records_parameter', 'measurement_unit')

        # Adding field 'Parameter.units'
        db.add_column(u'records_parameter', 'units',
                      self.gf('django.db.models.fields.CharField')(default='new unit', max_length=25),
                      keep_default=False)


        # Changing field 'Zone.url_id'
        db.alter_column(u'records_zone', 'url_id', self.gf('django.db.models.fields.IntegerField')())
        # Deleting field 'Station.lat'
        db.delete_column(u'records_station', 'lat')

        # Deleting field 'Station.active'
        db.delete_column(u'records_station', 'active')

        # Deleting field 'Station.lon'
        db.delete_column(u'records_station', 'lon')


    def backwards(self, orm):
        # Adding field 'Parameter.name_hebrew'
        db.add_column(u'records_parameter', 'name_hebrew',
                      self.gf('django.db.models.fields.CharField')(default='name', max_length=25),
                      keep_default=False)

        # Adding field 'Parameter.measurement_unit'
        db.add_column(u'records_parameter', 'measurement_unit',
                      self.gf('django.db.models.fields.CharField')(default='unit', max_length=25),
                      keep_default=False)

        # Deleting field 'Parameter.units'
        db.delete_column(u'records_parameter', 'units')


        # Changing field 'Zone.url_id'
        db.alter_column(u'records_zone', 'url_id', self.gf('django.db.models.fields.PositiveIntegerField')())
        # Adding field 'Station.lat'
        db.add_column(u'records_station', 'lat',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Station.active'
        db.add_column(u'records_station', 'active',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Station.lon'
        db.add_column(u'records_station', 'lon',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
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