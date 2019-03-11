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
        rate = self.request.GET.get('status', None)
        applicant = self.request.user
        role = applicant.groups.all().values('name') #用户所有的组
        role_name = [r['name'] for r in role] #提出组名
        queryset = super(DeployViewSet, self).get_queryset()

        # 根据传来的status值,判断是申请列表还是历史列表
        if rate and int(rate) <= 2:
            queryset = queryset.filter(status__lte=2)
        elif rate and int(rate) > 2:
            queryset = queryset.filter(status__gte=2)
        else:
            pass

        # 判断登陆用户是否是管理员，是则显示所有项目，否则只显示自己的项目
        if "ops" not in role_name:
            queryset = queryset.filter(applicant=applicant)
        return queryset


    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        data = request.data
        data['assign_to'] = request.user
        print(data)
        if int(data['status']) == 3:
            jenkins = JenkinsApi()
            number = jenkins.get_next_build_number(data['name'])
            jenkins.build_job(data['name'], parameters={'tag': data['version']})
            sleep(30)
            console_output = jenkins.get_build_console_output(data['name'], number)
            data['console_output'] = console_output
        Deploy.objects.filter(pk=pk).update(**data)
        return Response(status=status.HTTP_204_NO_CONTENT)

