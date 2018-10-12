from django.shortcuts import render

from  rest_framework import viewsets,mixins
from .models import Server,NetworkDevice,IP
from .serializers import ServerAutoReportSerializer,ServerSerializer,NetworkDeviceSerializer,IPSerializer

class ServerAutoReportViewset(mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerAutoReportSerializer

class ServerViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

class NetworkDeviceViewset(viewsets.ReadOnlyModelViewSet):
    queryset = NetworkDevice.objects.all()
    serializer_class = NetworkDeviceSerializer

class IpViewset(viewsets.ReadOnlyModelViewSet):
    queryset = IP.objects.all()
    serializer_class = IPSerializer












