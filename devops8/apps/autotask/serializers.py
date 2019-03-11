#!/usr/bin/python
#coding:utf-8

from rest_framework import serializers
from .models import Tasks


class TasksSerializer(serializers.ModelSerializer):
    """ 任务系统序列化类"""

    class Meta:
        model = Tasks
        fields = "__all__"


