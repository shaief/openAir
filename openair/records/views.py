from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, render_to_response
# from django.utils import simplejson
import json
import datetime
from openair.records.models import (Record, Parameter, Station, 
                                    get_param_time_range)


# def parameters(request):
#     stations = Station.record_set.all()
#     return render_to_response("records/parameters.html", {
#                 "stations": stations
#            })

def parameters(request):
    latest_record_list = Record.objects.all().order_by('station')[:10]
    context = {'latest_record_list': latest_record_list}
    return render(request, 'records/parameters.html', context)

def record_csv(request, param_name):
    model = get_object_or_404(Foo, param_name)
    data = Record.get_data() # should return csv formatted string
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
    measurements = '['+', '.join([str(x) for x in measurements])+']'
    context = {"measurements": measurements}
    return render(request, 'records/station_view.html', context)
