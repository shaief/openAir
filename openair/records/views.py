from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from openair.records.models import Record, \
    Parameter, \
    Station, \
    Zone, \
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

    for r in p.record_set.all().order_by('-id')[:100]:

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

    p.low_level = p.standard_yearly
    p.high_level = p.standard_hourly
    # -------------------------------------------------------------

    info = dict(abbr=p.abbr)

    if not p.low_level is None:
        info['low_level'] = p.low_level

    if not p.high_level is None:
        info['high_level'] = p.high_level

    if not p.standard_hourly is None:
        info['standard_hourly'] = p.standard_hourly

    if not p.standard_8hours is None:
        info['standard_8hours'] = p.standard_8hours

    if not p.standard_daily is None:
        info['standard_daily'] = p.standard_daily

    if not p.standard_yearly is None:
        info['standard_yearly'] = p.standard_yearly

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
    station_params = Parameter.objects. \
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
    allrecords_length = len(s.record_set.all().filter(parameter__abbr=abbr).order_by('-id'))

    if allrecords_length > 24:
        number_of_records = 24
    else:
        number_of_records = allrecords_length-1
    zone_list = Zone.objects.all().order_by('name')
    station_list = Station.objects.all().order_by('name')
    lastupdate = s.record_set.latest('id').timestamp
    twentyfourth = s.record_set.all().filter(parameter__abbr=abbr). \
        order_by('-id')[number_of_records].timestamp
    abbr_id = Parameter.objects.get(abbr=abbr).id
    p = Parameter.objects.get(abbr=abbr)
    # averages - total:
    total_average_value = Record.objects. \
        filter(parameter=abbr_id).aggregate(Avg('value'))
    average_value = Record.objects. \
        filter(parameter=abbr_id). \
        filter(station__url_id=url_id). \
        aggregate(Avg('value'))
    # averages - by time of the day:
    total_average_value_hour = Record.objects. \
        filter(parameter=abbr_id). \
        filter(timestamp__hour=lastupdate.hour). \
        aggregate(Avg('value'))
    average_value_hour = Record.objects. \
        filter(parameter=abbr_id). \
        filter(station__url_id=url_id). \
        filter(timestamp__hour=lastupdate.hour). \
        aggregate(Avg('value'))
    # list all the parameters in this station
    station_params = Parameter.objects. \
        filter(record__station__url_id=url_id).distinct()

    try:
        standardHourly = float(p.standard_hourly)
    except:
        standardHourly = -9999
    try:
        standard8Hours = float(p.standard_8hours)
    except:
        standard8Hours = -9999
    try:
        standardDaily = float(p.standard_daily)
    except:
        standardDaily = -9999
    try:
        standardYearly = float(p.standard_yearly)
    except:
        standardYearly = -9999
    try:
        average_value_hour = float(average_value_hour['value__avg'])
    except:
        average_value_hour = -9999
    try:
        total_average_value_hour = float(total_average_value_hour['value__avg'])
    except:
        total_average_value_hour = -9999

    # Context to render:
    context = dict(
        station=s,
        parameter=p,
        abbr=abbr,
        station_list=station_list,
        station_params=station_params,
        lastupdate=lastupdate,
        twentyfourth=twentyfourth,
        zone_list=zone_list,
        average_value=average_value['value__avg'],
        total_average_value=total_average_value['value__avg'],
        average_by_hour=average_value_hour,
        total_average_by_hour=total_average_value_hour,
        standardHourly=standardHourly,
        standard8Hours=standard8Hours,
        standardDaily=standardDaily,
        standardYearly=standardYearly,
    )
    return render(request, 'records/stationmapparam.html', context)


def stationmapwind(request, zone_url_id, station_url_id):
    s = get_object_or_404(Station, url_id=station_url_id)
    zone_list = Zone.objects.all().order_by('name')
    station_list = Station.objects.all().order_by('name')
    station_params = Parameter.objects. \
        filter(record__station__url_id=station_url_id).distinct()
    station_has_wind = Station.objects. \
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
    for r in s.record_set.all().order_by('-id')[:100]:
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
    allrecords_length = len(s.record_set.all().filter(parameter__abbr=abbr).order_by('-id'))
    print '{} all records_length'.format(allrecords_length)
    if allrecords_length > 24:
        number_of_records = 24
    else:
        number_of_records = allrecords_length-1
    records = []
    point = [s.lon, s.lat]
    number_of_values = 0
    sum_values = 0
    print '{} count records'.format(number_of_records)
    for r in s.record_set.all().filter(parameter__abbr=abbr).order_by('-id'):
        if (r.parameter.abbr == abbr):
            number_of_values += 1
            sum_values += r.value
            records.append(
                dict(
                    record_id=number_of_values,
                    value=r.value,
                    timestamp=r.timestamp.isoformat(),
                    day=r.timestamp.day,
                    month=r.timestamp.month,
                    year=r.timestamp.year,
                    hour=r.timestamp.hour,
                    minutes=r.timestamp.minute
                )
            )
            if number_of_values == number_of_records:
                break

    if number_of_values > 0:
        average_value = sum_values / number_of_values
    else:
        average_value = 'No measurements for ' + abbr
    number_of_values = 0
    data = dict(
        point=point,
        records=records,
        average_value=average_value
    )
    return HttpResponse(json.dumps(data))


def dailyparam_json(request, url_id, abbr):
    today = datetime.datetime.now()
    yesterday = datetime.datetime.now() + datetime.timedelta(days=-1)
    two_days_ago = datetime.datetime.now() + datetime.timedelta(days=-2)
    three_days_ago = datetime.datetime.now() + datetime.timedelta(days=-3)
    four_days_ago = datetime.datetime.now() + datetime.timedelta(days=-4)
    five_days_ago = datetime.datetime.now() + datetime.timedelta(days=-5)
    six_days_ago = datetime.datetime.now() + datetime.timedelta(days=-6)
    a_week_ago = datetime.datetime.now() + datetime.timedelta(days=-7)
    abbr_id = Parameter.objects.get(abbr=abbr).id
    today_avg = Record.objects. \
        filter(parameter=abbr_id). \
        filter(station__url_id=url_id). \
        filter(timestamp__range=(yesterday, today)). \
        aggregate(average=Avg('value'))
    yesterday_avg = Record.objects. \
        filter(parameter=abbr_id). \
        filter(station__url_id=url_id). \
        filter(timestamp__range=(two_days_ago, yesterday)). \
        aggregate(average=Avg('value'))
    two_days_ago_avg = Record.objects. \
        filter(parameter=abbr_id). \
        filter(station__url_id=url_id). \
        filter(timestamp__range=(three_days_ago, two_days_ago)). \
        aggregate(average=Avg('value'))
    three_days_ago_avg = Record.objects. \
        filter(parameter=abbr_id). \
        filter(station__url_id=url_id). \
        filter(timestamp__range=(four_days_ago, three_days_ago)). \
        aggregate(average=Avg('value'))
    four_days_ago_avg = Record.objects. \
        filter(parameter=abbr_id). \
        filter(station__url_id=url_id). \
        filter(timestamp__range=(five_days_ago, four_days_ago)). \
        aggregate(average=Avg('value'))
    five_days_ago_avg = Record.objects. \
        filter(parameter=abbr_id). \
        filter(station__url_id=url_id). \
        filter(timestamp__range=(six_days_ago, five_days_ago)). \
        aggregate(average=Avg('value'))
    six_days_ago_avg = Record.objects. \
        filter(parameter=abbr_id). \
        filter(station__url_id=url_id). \
        filter(timestamp__range=(a_week_ago, six_days_ago)). \
        aggregate(average=Avg('value'))
    data = dict(
        url_id=url_id,
        abbr=abbr,
        today_avg=today_avg['average'],
        yesterday_avg=yesterday_avg['average'],
        two_days_ago_avg=two_days_ago_avg['average'],
        three_days_ago_avg=three_days_ago_avg['average'],
        four_days_ago_avg=four_days_ago_avg['average'],
        five_days_ago_avg=five_days_ago_avg['average'],
        six_days_ago_avg=six_days_ago_avg['average'],
        daily_avg=[today_avg['average'],
                   yesterday_avg['average'],
                   two_days_ago_avg['average'],
                   three_days_ago_avg['average'],
                   four_days_ago_avg['average'],
                   five_days_ago_avg['average'],
                   six_days_ago_avg['average'],
        ]
    )
    return HttpResponse(json.dumps(data))


def stationmapwind_json(request, url_id):
    s = get_object_or_404(Station, url_id=url_id)
    rv = []
    i = 0
    point = [s.lon, s.lat]
    records = list(s.record_set.all().order_by('-id'))
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
        if i == 50:
            break
    data = dict(point=point, records=rv)
    return HttpResponse(json.dumps(data))


def stations_json(request):
    s = Station.objects.all().order_by('name')
    stations = []
    for sta in s:
        if not ((sta.lon is None) & (sta.lat is None)):
            if not ((sta.lon == 0.0) & (sta.lat == 0.0)):
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
