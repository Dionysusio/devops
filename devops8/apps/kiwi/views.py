#!/usr/bin/python
#coding:utf-8

from .serializers import IdcSerializer, FunctionSerializer, SubfunctionSerializer, AzSerializer
from .models import Idc, Function, Subfunction, AZ
from utils.ipm_api import ipm_data
import json
from django.views.generic import View
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import requests


class IdcViewSet(View):
    """
        get: 列出所有idc
        序列化并入库
    """

    def get(self, request):
        data = ipm_data()
        idcs = data.showidc()
        json_list = []
        for idc_obj in idcs:
            # print(idc_obj)
            json_dict = {}
            json_dict['name'] = idc_obj['name']
            json_dict['tree_id'] = idc_obj['tree_id']
            json_dict['idc_az'] = idc_obj['idc_az']
            json_list.append(json_dict)
        # json_list = json.dumps(json_list)
        print(json_list)
        for e in json_list:
            print(e)
            data = e
            serializer = IdcSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                content = JSONRenderer().render(serializer.data)
                # return HttpResponse(content, content_type="application/json")
        return HttpResponse(json_list,content_type="application/json")


class FunctionViewSet(View):
    """
        get:列出所有功能大类
            序列化并入库
    """
    # def get(self,request):
    #     data = ipm_data()
    #     functions = data.get_function()
    #     json_list = []
    #     for fun in functions:
    #         json_dict = {}
    #         json_dict['name'] =fun['name']
    #         json_dict['name_en'] =fun['name_en']
    #         json_dict['az'] = fun['az']
    #         json_list.append(json_dict)
    #     print(json_list)
    #     for e in json_list:
    #         # print(e)
    #         data = e
    #         serializer = FunctionSerializer(data=data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             content = JSONRenderer().render(serializer.data)
    #             return HttpResponse(content, content_type="application/json")
    #
    #     # return HttpResponse(json_list)


class SubfunctionViewSet(View):
    """
        get: 列出所有功能小类
             序列化并入库
    """
    pass


class AZViewSet(View):
    """
        get:列出所有可用区
            序列化并入库
    """

    pass



