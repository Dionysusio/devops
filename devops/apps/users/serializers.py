#!/usr/bin/python3
#coding:utf-8
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    """
    用户序列化类,和模型保持一致
    这里写的每个字段是我们要返回给前端的字段
    """
    id = serializers.IntegerField()
    username = serializers.CharField()
    # username 字段名是返回给前端的key名,serializers.CharField() 是返回的类型
    email = serializers.EmailField()








