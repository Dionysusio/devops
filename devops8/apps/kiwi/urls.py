#!/usr/bin/python
#coding:utf-8

from django.conf.urls import url
from .views import *

urlpatterns = [
    url('^idc_list/$', IdcViewSet.as_view(), name='project_list'),
    # url('^function/$', FunctionViewSet.as_view(), name='function'),
    # url('^subfunction/$', SubfunctionViewSet.as_view(), name='subfunction'),
    # url('^AZ/$', AZViewSet.as_view(), name='AZ')
]

