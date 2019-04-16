# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import Group
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

# from django.conf.settings import GITLAB_HTTP_URI, GITLAB_TOKEN
# import gitlab


# 序列化控制: 具体的实现

# 参考autoAdmin: 除了不支持创建,其他都支持
# https://github.com/Dionysusio/autoAdmin/blob/master/apps/users/serializers.py

class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化类
    """
    # 这里只做了个格式化时间,因为其他的提交了也没用,修改最终调用的是update,update方法里限制了只允许修改phone,is_active
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                            label="上次登录时间",
                                            help_text="上次登录时间")

    class Meta:
        model = User
        # 往前端返回的字段
        fields = ("id", "username", "name", "phone", "email", "is_active", "last_login")


    def update(self, instance, validated_data):
        # 默认所有的都可以修改,也可以在这里控制,这里定义了的才可以修改; 上面的序列化也可以控制:read_only=True
        instance.phone = validated_data.get("phone", instance.phone)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        return instance



# 支持用户注册,post请求; 还支持修改密码
# 参考autoAdmin: https://github.com/Dionysusio/autoAdmin/blob/master/apps/users/serializers.py

class UserRegSerializer(serializers.ModelSerializer):
    """
    用户注册序列化类
    """
    # style属性: 将明文密码转为密文
    password = serializers.CharField(style={"input_type": "password"},
                                     label="密码",
                                     write_only=True,
                                     help_text="密码")

    class Meta:
        model = User
        fields = ("username", "password", "name", "id", "phone")


    def validate(self, attrs):
        attrs["is_active"] = False #默认不可以登陆
        attrs["email"] = "{}{}".format(attrs['username'], settings.DOMAIN) #增加一个email地址
        return attrs

    def create(self, validated_data):
        instance = super(UserRegSerializer, self).create(validated_data=validated_data)
        instance.set_password(validated_data["password"])  #用户表的一个方法set_password,注释create,则创建的密码是明文的
        instance.save()
        return instance

        # 创建用户的同时创建gitlab用户
        # gl = gitlab.Gitlab(settings.GITLAB_HTTP_URI, settings.GITLAB_TOKEN, api_version=4)
        # res = gl.users.create({'username': validated_data['username'],
        #                        'password': validated_data['password'],
        #                        'email': validated_data['email'],
        #                        'name': validated_data['name']})
        # return instance

    def update(self, instance, validated_data):
        password = validated_data.get("password", None)
        if password:
            instance.set_password(password) # 和create 一样,先获取密码,然后set_password
            instance.save()
        return instance

