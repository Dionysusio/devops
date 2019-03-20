#!/usr/bin/python
#coding:utf-8

from rest_framework import viewsets, permissions, response, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
# from utils.jenkins_api import JenkinsApi
from django.contrib.auth import get_user_model
User = get_user_model()

from .serializers import DeploySerializer
from .models import Deploy
from .filters import DeployFilter



class DeployViewSet(viewsets.ModelViewSet):
    """
        list:
            获取上线列表

        retrieve:
            获取上线信息

        create:
            申请上线

        update:
            代码更新信息

        delete:
            取消上线

    """

    queryset = Deploy.objects.all()
    serializer_class = DeploySerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_class = DeployFilter
    filter_fields = ("name", "status")


    def get_queryset(self):
        # 根据申请人,提取出申请人所在的组(所有的)
        rate = self.request.GET.get('status', None)
        applicant = self.request.user #申请人
        role = applicant.groups.all().values('name') #(申请人)用户所有的组
        role_name = [r['name'] for r in role] #提取出组名
        queryset = super(DeployViewSet, self).get_queryset()

        # 根据传来的status值,判断是申请列表还是历史列表
        if rate and int(rate) <= 2:  #申请列表
            queryset = queryset.filter(status__lte=2)
        elif rate and int(rate) > 2: #历史列表,已经申请过的
            queryset = queryset.filter(status__gte=2)
        else:
            pass

        # 判断登陆用户是否为管理员，是 则显示所有项目，否则 只显示自己的项目
        # 根据组来判断,是否在一个有权限的组里 方便管理, 用户直接加入组中就拥有相应的权限
        if "ops" not in role_name:
            queryset = queryset.filter(applicant=applicant)
        return queryset


    def partial_update(self, request, *args, **kwargs):
        # 部分更新
        pk = kwargs.get("pk")
        data = request.data
        data['assign_to'] = request.user #上线人
        print(data)
        if int(data['status']) == 3:  #状态为3, 则进行 上线
            jenkins = JenkinsApi()  #调用jenkins api,进行上线
            number = jenkins.get_next_build_number(data['name']) #参数 项目名称
            jenkins.build_job(data['name'], parameters={'tag': data['version']})  #参数 项目名称, 项目版本
            sleep(30)
            console_output = jenkins.get_build_console_output(data['name'], number) # 参数 项目名称, number
            data['console_output'] = console_output
        Deploy.objects.filter(pk=pk).update(**data) #更新
        return Response(status=status.HTTP_204_NO_CONTENT)

