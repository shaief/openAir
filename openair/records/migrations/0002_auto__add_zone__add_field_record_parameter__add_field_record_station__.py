# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Zone'
        db.create_table(u'records_zone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal(u'records', ['Zone'])

        # Adding field 'Record.parameter'
        db.add_column(u'records_record', 'parameter',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='records', to=orm['records.Parameter']),
                      keep_default=False)

        # Adding field 'Record.station'
        db.add_column(u'records_record', 'station',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='records', to=orm['records.Station']),
                      keep_default=False)

        # Adding field 'Station.zone'
        db.add_column(u'records_station', 'zone',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='stations', to=orm['records.Zone']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Zone'
        db.delete_table(u'records_zone')

        # Deleting field 'Record.parameter'
        db.delete_column(u'records_record', 'parameter_id')

        # Deleting field 'Record.station'
        db.delete_column(u'records_record', 'station_id')

        # Deleting field 'Station.zone'
        db.delete_column(u'records_station', 'zone_id')


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
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'records'", 'to': u"orm['records.Parameter']"}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'records'", 'to': u"orm['records.Station']"}),
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
            'url_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stations'", 'to': u"orm['records.Zone']"})
        },
        u'records.zone': {
            'Meta': {'object_name': 'Zone'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'url_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['records']