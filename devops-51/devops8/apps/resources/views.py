# -*- coding: utf-8 -*-


from django.views import View
from django.http import HttpResponse
from resources.qcloud import cvm
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Server
from .serializers import ServerSerializer



class TestView(View):
    def get(self,request,*args,**kwargs):
        cvm.getCvmList()
        #让视图可以访问,测试代码是否正确
        return  HttpResponse('qcloud test')


class ServerViewset(ReadOnlyModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
