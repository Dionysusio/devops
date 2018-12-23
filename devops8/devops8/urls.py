#!/usr/bin/python3
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
# from rest_framework_jwt.views import obtain_jwt_token

from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from groupUsers .views import GroupUserViewset
from users.router import router as user_router
from groups.router import group_router
from permissions.router import permission_router
from resources.router import router as resources_router
# from resources import apscheduler


router = DefaultRouter()
# router.register("groupUsers", GroupUserViewset, base_name="groupUsers")
router.registry.extend(user_router.registry)
router.registry.extend(group_router.registry)
# router.registry.extend(resources_router.registry)
router.registry.extend(permission_router.registry)


urlpatterns = [
    url(r'^api/', include(router.urls)),
    # url(r'^', include(router.urls)),
    url(r'^', include('resources.urls')),
    # url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^docs/', include_docs_urls("Friedrich meer's docs")),
    # url(r'^api-token-auth/', obtain_jwt_token),

]
