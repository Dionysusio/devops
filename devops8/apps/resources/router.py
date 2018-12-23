#!/usr/bin/python
#coding:utf-8

from rest_framework.routers import DefaultRouter
from .views import ServerViewset


router = DefaultRouter()

router.register("Servers", ServerViewset, base_name="Servers")

