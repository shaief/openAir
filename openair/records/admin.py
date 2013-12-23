from django.contrib import admin
from .models import Zone, Station, Parameter, Record


# Zone and Station share the same ModelAdmin
class ZoneStationAdmin(admin.ModelAdmin):
	list_display = ['url_id', 'name']


class ParameterAdmin(admin.ModelAdmin):
	list_display = ['abbr', 'name', 'units']


class RecordAdmin(admin.ModelAdmin):
	list_display = ['parameter',
					'station',
					'station_url_id',
					'timestamp',
					'value']


admin.site.register([Zone, Station], ZoneStationAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(Record, RecordAdmin)