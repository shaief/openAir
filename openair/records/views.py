from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from openair.records.models import Record, Parameter, Station, \
    get_param_time_range
import datetime
import json
import random
import time
import itertools


def parameters(request):
    latest_record_list = Record.objects.all().order_by('station')[:10]
    context = {'latest_record_list': latest_record_list}
    return render(request, 'records/parameters.html', context)


def parameter(request, abbr):

    p = get_object_or_404(Parameter, abbr=abbr)
    context = dict(parameter=p)
    return render(request, 'records/parameter.html', context)


def parameter_json(request, abbr):

    p = get_object_or_404(Parameter, abbr=abbr)

    records = []

    zones = []

    for r in p.record_set.all().order_by('timestamp'):

        if not r.station.name in \
                [record['name'] for record in records]:
            records.append(dict(name=r.station.name,
                                zone=r.station.zone.name,
                                zone_id=r.station.zone.url_id,
                                value=r.value))

            if not r.station.zone.url_id in \
                    [z['zone_id'] for z in zones]:
                zones.append(dict(zone=r.station.zone.name,
                                  zone_id=r.station.zone.url_id))

    # -------------------------------------------------------------
    # temporarily the standard levels are generated based on
    # the records. TODO: add this functionality to the model!
    min_record = min([r['value'] for r in records])
    max_record = max([r['value'] for r in records])
    records_range = max_record - min_record
    boundery = 0.25

    # add a chance to don't have low level
    if (random.random() > 0.2):
        p.low_level = min_record + boundery * records_range
    else:
        p.low_level = None

    # add a chance to don't have low level
    if (random.random() > 0.2):
        p.high_level = max_record - boundery * records_range
    else:
        p.high_level = None
    # -------------------------------------------------------------

    info = dict(abbr=p.abbr)

    if not p.low_level is None:
        info['low_level'] = p.low_level

    if not p.high_level is None:
        info['high_level'] = p.high_level

    data = dict(info=info, records=records, zones=zones)

    return HttpResponse(json.dumps(data))

def map(request):

    return render(request, 'records/map.html')

def stationmap(request, url_id):
    s = get_object_or_404(Station, url_id=url_id)
    station_list = Station.objects.all().order_by('name')
    context = dict(station=s, station_list=station_list)
    return render(request, 'records/stationmap.html', context)

def stationmapparam(request, url_id, abbr):
    s = get_object_or_404(Station, url_id=url_id)
    station_list = Station.objects.all().order_by('name')
    context = dict(station=s, abbr=abbr, station_list=station_list)
    return render(request, 'records/stationmapparam.html', context)

def stationmapwind(request, zone_url_id, station_url_id):
    s = get_object_or_404(Station, url_id=station_url_id)
    station_list = Station.objects.all().order_by('name')
    context = dict(station=s, abbr='WD', station_list=station_list, zone_url_id=zone_url_id)
    return render(request, 'records/stationmapwind_pi.html', context)

def stationmap_json(request, url_id):
    s = get_object_or_404(Station, url_id=url_id)
    records = []
    values = []
    params = []
    for r in s.record_set.all().order_by('timestamp'):
        if not r.parameter.abbr in \
                [record['name'] for record in records]:
            records.append(dict(name=r.parameter.abbr,
                                value=r.value,
                                ))
    geom = [s.lon, s.lat]
    info = dict(records=records, geom=geom, timestamp=str(r.timestamp))

    data = dict(params=params, values=values,
                geom=geom, timestamp=str(r.timestamp))
    return HttpResponse(json.dumps(info))

def stationmap_param_json(request, url_id, abbr):
    s = get_object_or_404(Station, url_id=url_id)
    records = []
    for r in s.record_set.all().order_by('timestamp'):
        if (r.parameter.abbr == abbr):
            records.append(dict(value=r.value,
                                timestamp=str(r.timestamp
                                )))                  
    data = dict(records=records)                       
    return HttpResponse(json.dumps(data))

def stationmapwind_json(request, url_id):
    s = get_object_or_404(Station, url_id=url_id)
    rv = []
    i = 0
    records = list(s.record_set.all().order_by('timestamp'))
    l = itertools.groupby(records, lambda x: x.timestamp)
    for ts, records in l:
        i+=1
        params = {x.parameter.abbr: x.value for x in records}
        d = {
             'id': i,
             'direction': params['WD'],
             'speed': params['WS'],
             'timestamp': unicode(ts),
             }
        rv.append(d)
#         wind = {
#                 'WD':r.parameter_set,
#                  'WS':0}
#                 wind['WD'] = r.value
#             else:
#                 wind['WS'] = r.value
#         records.append(dict(abbr=r.parameter.abbr, value=r.value,
#                             timestamp=str(r.timestamp), id=i,
#                             wind=wind
#                                 ))
    data = dict(records=rv)    
    return HttpResponse(json.dumps(data))

def record_csv(request, param_name):
    model = get_object_or_404(Foo, param_name)
    data = Record.get_data()  # should return csv formatted string
    return HttpResponse(data, content_type='text/csv')


def zones(request):
    latest_zone_list = Record.objects.all().order_by('-timestamp')[:5]
    context = {'latest_zone_list': latest_zone_list}
    return render(request, 'records/zones.html', context)

'''
TODO: create a view that passes data from DB to json
according to query/view. This JSON will be parsed later to
a beautiful D3 visualization.

def my_ajax_view(request):
    if not request.is_ajax():
        raise Http404
    data_dict = getmydata() #let's suppose is a dict
    return HttpResponse(json.dumps(data_dict))
'''


def station(request, station_id, start, end):
    # accessible over: station-1-2013-to-2014
    start = datetime.date(2013, 1, 1)
    end = datetime.date(2014, 1, 1)
    wd = Parameter.objects.first()
    wd_rec = get_param_time_range(wd, start, end)
    tstamps, measurements = zip(*[(x.timestamp, x.value) for x in wd_rec])
    measurements = '[' + ', '.join([str(x) for x in measurements]) + ']'
    context = {"measurements": measurements}
    return render(request, 'records/station_view.html', context)


def demo_linechart(request, station_id, start, end):
    """
    lineChart page
    """
    start_time = int(time.mktime(datetime.datetime(2012, 6, 1).timetuple())
                     * 1000)
    nb_element = 150
    xdata = range(nb_element)
    xdata = map(lambda x: start_time + x * 1000000000, xdata)
    ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    ydata2 = map(lambda x: x * 2, ydata)

    tooltip_date = "%d %b %Y %H:%M:%S %p"
    extra_serie1 = {
        "tooltip": {"y_start": "", "y_end": " cal"},
        "date_format": tooltip_date,
        'color': '#a4c639'
    }
    extra_serie2 = {
        "tooltip": {"y_start": "", "y_end": " cal"},
        "date_format": tooltip_date,
        'color': '#FF8aF8'
    }
    chartdata = {'x': xdata,
                 'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie1,
                 'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie2}

    charttype = "lineChart"
    chartcontainer = 'linechart_container'  # container name
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '%d %b %Y %H',
            'tag_script_js': True,
            'jquery_on_ready': False,
        }
    }
    return render(request, 'records/station_view.html', data)
    # return render_to_response('linechart.html', data)
