#!/usr/bin/python
#coding:utf-8

from rest_framework.routers import DefaultRouter
from .views import IdcViewSet, FunctionViewSet, SubfunctionViewSet,AZViewSet

kiwi_router = DefaultRouter()

kiwi_router.register("idc_list", IdcViewSet, base_name="idc_list")
# kiwi_router.register("function", FunctionViewSet, base_name="function")
# kiwi_router.register("subfunction", SubfunctionViewSet, base_name="subfunction")
# kiwi_router.register("AZ", AZViewSet, base_name="AZ")

