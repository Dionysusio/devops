#!/usr/bin/python
#coding:utf-8

from rest_framework.routers import DefaultRouter
from .views import DeployViewSet

deploy_router = DefaultRouter()
deploy_router.register("deploy", DeployViewSet, base_name="deploy")
