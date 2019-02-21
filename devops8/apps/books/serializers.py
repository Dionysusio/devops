#!/usr/bin/python3
#coding:utf-8

from rest_framework import serializers
from .models import Publish, Author, Book
from django.conf import settings


class PublishSerializer(serializers.ModelSerializer):
    """ 出版商序列化 """

    class Meta:
        model = Publish
        fields = ("id", "name", "city", "address")


class AuthorSerializer(serializers.ModelSerializer):
    """ 作者序列化 """
    class Meta:
        model = Author
        fields = ("id", "name", "email", "phone", "address")


class BookSerializer(serializers.ModelSerializer):
    """ 书序列化"""
    class Meta:
        model = Book
        fields = "__all__"

    def author(self, author_queryset): #author_queryset: book.authors.all()
        ret = []
        print(author_queryset)
        # 多对多的结果是一个列表对象，需要遍历对象，将需要序列化的内容提出来即可,返回书对应的所有作者
        for author in author_queryset:
            ret.append({
                'id': author.id,
                'name': author.name,
                'email': author.email
            })
        return ret

    def to_representation(self, instance):
        # 一对多关系，相当于一对多的正向查询。获取当前书的出版商，
        publisher_obj = instance.publisher

        # 多对多，相当于多对多的正向查询。获取当前书对应的作者，
        # instance 指的是book
        authors_obj = self.author(instance.authors.all())

        # 将书的相关信息序列化，即将Book.objects.all()的querydict结果集合转为JSON
        ret = super(BookSerializer, self).to_representation(instance)

        # 将关联表需要序列化输出的列处理为json,也加入序列化大字典中。这样就能序列化出当前表和关联表所有想展示的字段了
        ret["publisher"] = {
            "id": publisher_obj.id,
            "name": publisher_obj.name,
            "address": publisher_obj.address
        },

        ret["authors"] = authors_obj
        return ret

    # def to_internal_value(self, data):
    #     print(data)

    # 重写create方法，源码中已经对单表、一对多、多对多对关系做了处理，此次为了学习调试方便重写
    def create(self, validated_data):
        # {'name': '平凡的世界', 'publication_date': datetime.date(2018, 5, 10),
        # 'publisher': <Publish: Publish object>, 'authors': [<Author: Author object>]}

        author_list = validated_data.pop('authors', [])  #把前端传递过来的authors字段置空
        instance = self.Meta.model.objects.create(**validated_data)
        # print(validated_data)
        # author和book是多对多关系，添加数据时需要单独处理
        instance.authors.set(author_list)
        return instance

    # 源码中已经对单表、一对多、多对多对关系做了处理，此次为了学习调试方便重写
    def update(self, instance, validated_data):
        print(validated_data)
        author_list = validated_data.pop('authors', [])
        self.Meta.model.objects.filter(id=instance.id).update(**validated_data)
        print(author_list)
        # 多对多添加的两种写法
        instance.authors.set(author_list)
        return instance


