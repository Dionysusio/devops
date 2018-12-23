from django.shortcuts import render

from  rest_framework import viewsets,mixins
from .models import Server,NetworkDevice,IP
from .serializers import ServerAutoReportSerializer,ServerSerializer,NetworkDeviceSerializer,IPSerializer

class ServerAutoReportViewset(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
        create:创建一个服务器
    """
    queryset = Server.objects.all()
    serializer_class = ServerAutoReportSerializer

class ServerViewset(viewsets.ReadOnlyModelViewSet):
    """
        list:列出所有服务器信息
        retrieve:读取一个服务器信息
    """
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

class NetworkDeviceViewset(viewsets.ReadOnlyModelViewSet):
    """
        list:列出所有网卡信息
        retrieve:读取一个网卡信息
    """
    queryset = NetworkDevice.objects.all()
    serializer_class = NetworkDeviceSerializer

class IpViewset(viewsets.ReadOnlyModelViewSet):
    """
        list:列出所有服务器信息
        retrieve:读取一个服务器信息
    """
    queryset = IP.objects.all()
    serializer_class = IPSerializer


