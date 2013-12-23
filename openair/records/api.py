from tastypie import fields
from tastypie.resources import ModelResource
from .models import Station
from tastypie.serializers import Serializer
from .models import Station, Record, Parameter



class ParameterResource(ModelResource):
    
    class Meta:
        queryset = Parameter.objects.all()
        resource_name = 'parameter'
        serializer = Serializer(formats=['json'])

class RecordResource(ModelResource):
    parameter = fields.ToOneField(ParameterResource, 'parameter', full=True)
    class Meta:
        queryset = Record.objects.all()
        resource_name = 'record'
        serializer = Serializer(formats=['json'])

class StationResource(ModelResource):
    records = fields.ToManyField(RecordResource, 'record_set', full=True)
    class Meta:
        queryset = Station.objects.all()
        resource_name = 'station'
        serializer = Serializer(formats=['json'])
