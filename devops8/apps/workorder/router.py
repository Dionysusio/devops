#!/usr/bin/python
#coding:utf-8

from rest_framework.routers import DefaultRouter
from .views import WorkOrderViewset


workorder_router = DefaultRouter()
workorder_router.register('workorder',WorkOrderViewset,base_name="workorder")
