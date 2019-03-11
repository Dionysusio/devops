#!/usr/bin/python
#coding:utf-8

from rest_framework.routers import DefaultRouter
from .views import TasksViewSet

autotask_router = DefaultRouter()

autotask_router.register("autotask", TasksViewSet, base_name="autotask")


