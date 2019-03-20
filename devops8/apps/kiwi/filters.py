#!/usr/bin/python
#coding:utf-8

import django_filters
from .models import Idc, Function, Subfunction, AZ


class IdcFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr='contains')
    tree_id = django_filters.CharFilter(field_name="tree_id", lookup_expr='contains')

    class Meta:
        model = Idc
        fields = ["name", "tree_id"]


class FunctionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr='contains')
    az   = django_filters.CharFilter(field_name="az", lookup_expr='contains')

    class Meta:
        model = Function
        fields = ["name", "az"]


class SubfunctionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr='contains')
    function = django_filters.CharFilter(field_name="function", lookup_expr='contains')

    class Meta:
        model = Subfunction
        fields = ["name", "function"]


class AZFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr='contains')
    idc = django_filters.CharFilter(field_name="idc", lookup_expr='contains')

    class Meta:
        model = AZ
        fields = ["name", "idc"]

