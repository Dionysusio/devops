#!/usr/bin/python3
#coding:utf-8

import django_filters
from .models import Publish, Author, Book


class PublishFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr='contains')
    city = django_filters.CharFilter(field_name="city", lookup_expr='contains')

    class Meta:
        model = Publish
        fields = ["name", "city"]

class AuthorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr='contains')
    email = django_filters.CharFilter(field_name="email", lookup_expr='contains')

    class Meta:
        model = Author
        fields = ["name", "email"]

class BookFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr='contains')
    publisher = django_filters.CharFilter(field_name="publisher__name", lookup_expr='contains')
    authors = django_filters.CharFilter(field_name="authors__name", lookup_expr='contains')

    class Meta:
        model = Book
        fields = ["name", "authors", "publisher"]


