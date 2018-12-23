#!/usr/bin/python3
#coding:utf-8

from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^idcs/$',views.idc_list),
    url(r'^idcs/(?P<pk>[0-9]+)$',views.idc_detail),

]

########################### 版本二 ##############################################
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$',views.api_root),
    url(r'^idcs/$',views.idc_list_v2,name="idc-list"),
    url(r'^idcs/(?P<pk>[0-9]+)$',views.idc_detail_v2,name="idc-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)


########################### 版本三 ##############################################
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$',views.api_root),
    url(r'^idcs/$',views.IdcList.as_view(),name="idc-list"),
    url(r'^idcs/(?P<pk>[0-9]+)$',views.IdcDetail.as_view(),name="idc-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)


########################### 版本四 ##############################################
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$',views.api_root),
    url(r'^idcs/$',views.IdcList_V4.as_view(),name="idc-list"),
    url(r'^idcs/(?P<pk>[0-9]+)$',views.IdcDetail_V4.as_view(),name="idc-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)


########################### 版本五 ##############################################

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$',views.api_root),
    url(r'^idcs/$',views.IdcList_V5.as_view(),name="idc-list"),
    url(r'^idcs/(?P<pk>[0-9]+)$',views.IdcDetail_V5.as_view(),name="idc-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)

########################### 版本六 ##############################################


idc_list = views.IdcListViewset.as_view({
    "get": "list", #如果是get请求,就路由到list方法
    "post": "create"
})

idc_detail = views.IdcListViewset.as_view({
    "get": "retrieve",
    "put": "update",
    "delete": "destroy"
})

urlpatterns = [
    url("^$", views.api_root),
    url(r"^idcs/$", idc_list, name="idc-list"),
    url(r"^idcs/(?P<pk>[0-9]+)/$", idc_detail, name="idc-detail")
]

########################### 版本七 ##############################################

from rest_framework.routers import DefaultRouter #导入DefaultRouter

router = DefaultRouter() #实例化
router.register("idcs",views.IdcListViewset_v7) #注册,每次只要注册这个就可以了

urlpatterns = [
    url(r'^',include(router.urls))
    #router.urls自动帮我们处理url

]





