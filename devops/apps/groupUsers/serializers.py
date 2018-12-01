#!/usr/bin/python3
#coding:utf-8

from rest_framework import serializers
from django.contrib.auth.models import Group

class GroupSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	name = serializers.CharField(required=False)
