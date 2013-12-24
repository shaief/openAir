from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, render_to_response
from django.utils import simplejson
from openair.records.models import Record, Station


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
    data_dict = getmydata() #lets supose is a dict
    return HttpResponse(simplejson.dumps(data_dict))
'''
