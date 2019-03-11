#!/usr/bin/python
#coding:utf-8

from rest_framework import viewsets, permissions, response, status
from .serializers import TasksSerializer
from .models import Tasks
from .filters import TasksFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.ansible_api_simple import ANSRunner
import json


class TasksViewSet(viewsets.ModelViewSet):
    """
        list:
            列出所有任务

        retrieve:
            某个任务的详细信息

        create:
            创建任务

        update:
            更新任务

        delete:
            删除任务

    """
    permission_classes = (permissions.IsAuthenticated,)

    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    filter_class = TasksFilter
    filter_fields = ("name", "status")


    def partial_update(self, request, *args, **kwargs):
        # 获取这条任务的id
        pk = int(kwargs.get("pk"))
        data = request.data
        # print(data)
        task = Tasks.objects.get(pk=pk)  # 拿到任务
        rbt = ANSRunner()  # 调用ansible api
        # print(task.playbook.path)
        rbt.run_playbook(task.playbook.path)  # ansible执行任务,只接受一个参数,playbook的文件位置
        data['detail_result'] = json.dumps(rbt.get_playbook_result(), indent=4) #拿到执行结果
        Tasks.objects.filter(pk=pk).update(**data)  # 存到数据库
        return response.Response(status=status.HTTP_204_NO_CONTENT)


