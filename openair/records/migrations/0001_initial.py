# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Record'
        db.create_table(u'records_record', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'records', ['Record'])

        # Adding model 'Station'
        db.create_table(u'records_station', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lon', self.gf('django.db.models.fields.FloatField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')()),
            ('url_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'records', ['Station'])

        # Adding model 'Parameter'
        db.create_table(u'records_parameter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('abbr', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('name_hebrew', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('measurement_unit', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal(u'records', ['Parameter'])


    def backwards(self, orm):
        # Deleting model 'Record'
        db.delete_table(u'records_record')

        # Deleting model 'Station'
        db.delete_table(u'records_station')

        # Deleting model 'Parameter'
        db.delete_table(u'records_parameter')


    models = {
        u'records.parameter': {
            'Meta': {'object_name': 'Parameter'},
            'abbr': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measurement_unit': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'name_hebrew': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'records.record': {
            'Meta': {'object_name': 'Record'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'records.station': {
            'Meta': {'object_name': 'Station'},
            'active': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'url_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['records']