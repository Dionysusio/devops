#!/usr/bin/python3
#coding:utf-8

from rest_framework import viewsets, permissions
from .serializers import PublishSerializer, AuthorSerializer, BookSerializer
from .models import Publish, Author, Book
from .filters import PublishFilter,AuthorFilter,BookFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class PublishViewSet(viewsets.ModelViewSet):
    """
        list:
            列出所有出版商

        retrieve:
            某个出版商的详细信息

        create:
            创建出版商

        update:
            更新出版商

        delete:
            删除出版商

    """
    permission_classes = (permissions.IsAuthenticated,)

    queryset = Publish.objects.all()
    serializer_class = PublishSerializer
    pagination_class = PageNumberPagination
    filter_class = PublishFilter
    filter_fields = ("name", "city")


class AuthorViewSet(viewsets.ModelViewSet):
    """
        list:
            列出所有作者

        retrieve:
            某个作者的详细信息

        create:
            创建作者

        update:
            更新作者

        delete:
            删除作者

    """
    permission_classes = (permissions.IsAuthenticated,)

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = PageNumberPagination
    filter_class = AuthorFilter
    filter_fields = ("name", "email")


class BookViewSet(viewsets.ModelViewSet):
    """
        list:
            列出所有图书信息

        retrieve:
            某个图书的详细信息

        create:
            创建图书

        update:
            更新图书

        delete:
            删除图书

    """
    permission_classes = (permissions.IsAuthenticated,)

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = PageNumberPagination
    filter_class = BookFilter
    #跨关联搜索publisher__name,authors__name
    filter_fields = ("name", "publisher__name", "authors__name")


