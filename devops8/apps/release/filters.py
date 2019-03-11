#!/usr/bin/python
#coding:utf-8

import django_filters
from .models import Deploy

class DeployFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr='contains')
    status = django_filters.CharFilter(field_name="status", lookup_expr='contains')

    class Meta:
        model = Deploy
        fields = ["name", "status"]