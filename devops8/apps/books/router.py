#!/usr/bin/python3
#coding:utf-8

from rest_framework.routers import DefaultRouter
from .views import PublishViewSet, AuthorViewSet,BookViewSet

router = DefaultRouter()

router.register("publish", PublishViewSet, base_name="publish")
router.register("author", AuthorViewSet, base_name="author")
router.register("book", BookViewSet, base_name="book")



