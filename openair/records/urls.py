from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from openair.records import views
from tastypie.api import Api
from openair.records.api import StationResource

v0_api = Api(api_name='v0')
v0_api.register(StationResource())

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="records/index.html"),
        name='home'),
    url(r'^parameters/$', views.parameters, name='parameters'),

    url(r'^parameter/(?P<abbr>[-_()a-zA-Z0-9. ]+)/$', views.parameter,
        name='parameter'),
    url(r'^parameter/(?P<abbr>[-_()a-zA-Z0-9. ]+)/json/$', views.parameter_json,
        name='parameter_json'),
    #url(r'^station-(?P<station_id>\d+)-(?P<start>\d+)-to-(?P<end>\d+)$',
        #views.demo_linechart),
    # =====================================================================
    # urls for stationmap view, including jsons:
    url(r'^stationmap/json/(?P<url_id>[0-9]+)/(?P<abbr>[-_()a-zA-Z0-9.]+)/$',
            views.stationmap_param_json, name='stationmap_param_json'),
    url(r'^stationmap/json/(?P<url_id>[0-9]+)/$',
            views.stationmap_json, name='stationmap_json'),
    url(r'^stationmap/(?P<url_id>[0-9]+)/$',
            views.stationmap, name='stationmap'),
    url(r'^stationparams/(?P<url_id>[0-9]+)/$',
            views.stationparams, name='stationparams'),
    url(r'^stationmapparam/(?P<url_id>[0-9]+)/(?P<abbr>[-_ ()a-zA-Z0-9.]+)/$',
            views.stationmapparam, name='stationmap_param'),
    url(r'^stationmapwind/(?P<zone_url_id>[0-9]+)/(?P<station_url_id>[0-9]+)/$',
            views.stationmapwind, name='stationmapwind'),
    url(r'^stationmapwind/json/(?P<url_id>[0-9]+)/$',
            views.stationmapwind_json, name='stationmapwind_json'),
    # =====================================================================
    url(r'^map/$', views.map, name='map'),
    url(r'^indexmap/$',
        TemplateView.as_view(template_name='records/indexmap.html'),
        name='indexmap'),
    url(r'^zones/$', views.zones, name='zones'),
    url(r'^api/', include(v0_api.urls)),
    # =====================================================================
    url(r'^stations/json/$', views.stations_json, name='stations_json'),
)
