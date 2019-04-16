# -*- coding: utf-8 -*-
from django.views import View
from django.http import HttpResponse
from resources.qcloud import cvm
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Server
from .serializers import ServerSerializer
# from resources.apscheduler import scheduler
# import datetime


# def runjob():
#     print('jobrun is run:  {}'.format(datetime.datetime.now()))

class TestView(View):
    def get(self,request,*args,**kwargs):
        # 动态添加任务
        # scheduler.add_job(runjob,run_date=datetime.datetime.now(), id="runjob")
        # cvm.getCvmList()
        #让视图可以访问,测试代码是否正确
        return  HttpResponse('qcloud')

class ServerViewset(ReadOnlyModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

