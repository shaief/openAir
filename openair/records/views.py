from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from openair.records.models import Record, Parameter, Station, Zone, \
    get_param_time_range
import datetime
import json
import random
import time
import itertools

from django.db.models import Avg


def parameters(request):
    latest_record_list = Record.objects.all().order_by('station')[:10]
    context = {'latest_record_list': latest_record_list}
    return render(request, 'records/parameters.html', context)


def parameter(request, abbr):
    parameter_list = Parameter.objects.all()
    p = get_object_or_404(Parameter, abbr=abbr)
    lastupdate = p.record_set.latest('id').timestamp
    context = dict(
        parameter=p,
        parameter_list=parameter_list,
        lastupdate=lastupdate
    )
    return render(request, 'records/parameter.html', context)


def parameter_json(request, abbr):

    p = get_object_or_404(Parameter, abbr=abbr)

    records = []

    zones = []

    for r in p.record_set.all().order_by('timestamp'):

        if not r.station.name in \
                [record['name'] for record in records]:
            records.append(dict(
                name=r.station.name,
                zone=r.station.zone.name,
                datestamp=(r.timestamp).strftime("%d-%m-%Y"),
                timestamp=(r.timestamp).strftime("%H:%M"),
                datetimestamp=(r.timestamp).strftime("%H:%M %d-%m-%Y"),
                station_id=r.station.url_id,
                zone_id=r.station.zone.url_id,
                value=r.value)
            )

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


def stationparams(request, url_id):
    s = get_object_or_404(Station, url_id=url_id)
    station_list = Station.objects.all().order_by('name')
    parameter_list = s.record_set.all()
    station_params = Parameter.objects. \
        filter(record__station__url_id=url_id).distinct()
    lastupdate = s.record_set.latest('id').timestamp
    context = dict(
        station=s,
        station_list=station_list,
        parameter_list=parameter_list,
        lastupdate=lastupdate,
        station_params=station_params
    )
    return render(request, 'records/stationparams.html', context)


def stationmap(request, url_id):
    s = get_object_or_404(Station, url_id=url_id)
    zone_list = Zone.objects.all().order_by('name')
    station_list = Station.objects.all().order_by('name')
    station_params = Parameter.objects.\
        filter(record__station__url_id=url_id).distinct()
    lastupdate = s.record_set.latest('id').timestamp
    context = dict(
        station=s,
        station_list=station_list,
        zone_list=zone_list,
        station_params=station_params,
        lastupdate=lastupdate
    )
    return render(request, 'records/stationmap.html', context)


def stationmapparam(request, url_id, abbr):
    s = get_object_or_404(Station, url_id=url_id)
    zone_list = Zone.objects.all().order_by('name')
    station_list = Station.objects.all().order_by('name')
    lastupdate = s.record_set.latest('id').timestamp
    abbr_id = Parameter.objects.get(abbr=abbr).id
    total_average_value = Record.objects.\
        filter(parameter=abbr_id).aggregate(Avg('value'))
    station_params = Parameter.objects.\
        filter(record__station__url_id=url_id).distinct()
    context = dict(
        station=s,
        abbr=abbr,
        station_list=station_list,
        station_params=station_params,
        lastupdate=lastupdate,
        zone_list=zone_list,
        total_average_value=total_average_value['value__avg']
    )
    return render(request, 'records/stationmapparam.html', context)


def stationmapwind(request, zone_url_id, station_url_id):
    s = get_object_or_404(Station, url_id=station_url_id)
    zone_list = Zone.objects.all().order_by('name')
    station_list = Station.objects.all().order_by('name')
    station_params = Parameter.objects.\
        filter(record__station__url_id=station_url_id).distinct()
    station_has_wind = Station.objects.\
        filter(record__parameter__abbr='WD').distinct().order_by('name')
    context = dict(station=s,
                   abbr='WD',
                   station_list=station_list,
                   station_has_wind=station_has_wind,
                   zone_list=zone_list,
                   zone_url_id=int(zone_url_id),
                   station_params=station_params,
                   lat=s.lat, lon=s.lon
                   )
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

    info = dict(
        records=records,
        geom=geom,
        timestamp=(r.timestamp).strftime("%H:%M %d-%m-%Y")
    )

    data = dict(
        params=params,
        values=values,
        geom=geom,
        timestamp=str(r.timestamp)
    )
    return HttpResponse(json.dumps(info))


def stationmap_param_json(request, url_id, abbr):
    s = get_object_or_404(Station, url_id=url_id)
    records = []
    point = [s.lon, s.lat]
    number_of_values = 0
    sum_values = 0
    for r in s.record_set.get(parameter=abbr).order_by('timestamp')[:24]:
        if (r.parameter.abbr == abbr):
            number_of_values += 1
            sum_values += r.value
            records.append(
                dict(
                    value=r.value,
                    timestamp=r.timestamp.isoformat(),
                    day=r.timestamp.day,
                    month=r.timestamp.month,
                    year=r.timestamp.year,
                    hour=r.timestamp.hour,
                    minutes=r.timestamp.minute
                )
            )
    if number_of_values > 0:
        average_value = sum_values / number_of_values
    else:
        average_value = 'No measurements for ' + abbr
    data = dict(
        point=point,
        records=records,
        average_value=average_value
    )
    return HttpResponse(json.dumps(data))


def stationmapwind_json(request, url_id):
    s = get_object_or_404(Station, url_id=url_id)
    rv = []
    i = 0
    point = [s.lon, s.lat]
    records = list(s.record_set.all().order_by('timestamp'))
    l = itertools.groupby(records, lambda x: x.timestamp)
    for ts, records in l:
        i += 1
        params = {x.parameter.abbr: x.value for x in records}
        d = {
             'id': i,
             'direction': params['WD'],
             'speed': params['WS'],
             'timestamp': unicode(ts),
             }
        rv.append(d)
    data = dict(point=point, records=rv)
    return HttpResponse(json.dumps(data))


def stations_json(request):
    s = Station.objects.all().order_by('name')
    stations = []
    for sta in s:
        if not((sta.lon is None) & (sta.lat is None)):
            if not((sta.lon == 0.0) & (sta.lat == 0.0)):
                type = "Feature"
                properties = dict(
                    name=sta.name,
                    url_id=sta.url_id,
                    zone=sta.zone.name,
                    zone_url_id=sta.zone.url_id,
                    location=sta.location,
                )
                geometry = dict(
                    type="Point",
                    coordinates=[sta.lon, sta.lat]
                )
                stations.append(dict(
                    type=type,
                    properties=properties,
                    geometry=geometry,
                    name=sta.name,
                    url_id=sta.url_id,
                    zone=sta.zone.name,
                    zone_url_id=sta.zone.url_id,
                    location=sta.location,
                )
                )
    data = dict(type="FeatureCollection", features=stations)
    return HttpResponse(json.dumps(data))


def record_csv(request, param_name):
    model = get_object_or_404(Foo, param_name)
    data = Record.get_data()  # should return csv formatted string
    return HttpResponse(data, content_type='text/csv')


def zones(request):
    latest_zone_list = Zone.objects.all().order_by('name')
    context = {'latest_zone_list': latest_zone_list}
    return render(request, 'records/zones.html', context)
