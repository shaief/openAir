from tastypie.resources import ModelResource
from .models import Station
from tastypie.serializers import Serializer

class StationResource(ModelResource):
    class Meta:
        queryset = Station.objects.all()
        resource_name = 'station'
        serializer = Serializer(formats=['json'])