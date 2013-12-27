from django.contrib import admin
from .models import Zone, Station, Parameter, Record


class StationInline(admin.StackedInline):
    model = Station
    fieldsets = (
        (None, {
            'fields': ('url_id',)
        }),
        ('Station information', {
            'classes': ('collapse',),
            'fields': ('location', 'owners', 'date_of_founding',
                       'lon', 'lat', 'height')
        }),
    )
    readonly_fields = ('url_id',)
    can_delete = False
    extra = 0


class ZoneAdmin(admin.ModelAdmin):
    list_display = ('url_id', 'name')
    readonly_fields = ('url_id', 'name')
    inlines = (StationInline,)


class ParameterAdmin(admin.ModelAdmin):
    list_display = ('abbr', 'name', 'units')


class RecordAdmin(admin.ModelAdmin):
    list_display = ('parameter',
                    'station',
                    'timestamp',
                    'value')


admin.site.register(Zone, ZoneAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(Record, RecordAdmin)
