# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import Group
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

# from django.conf.settings import GITLAB_HTTP_URI, GITLAB_TOKEN
# import gitlab


# 序列化控制: 具体的实现
# 用户列表
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
        fields = ("id", "username", "name", "phone", "email", "is_active", "last_login")


    def update(self, instance, validated_data):
        # 默认所有的都可以修改,也可以在这里控制,这里定义了的才可以修改; 上面的序列化也可以控制:read_only=True
        instance.phone = validated_data.get("phone", instance.phone)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        return instance

# github 上autoAdmin的: 除了不支持创建,其他都支持
# class UserSerializer(serializers.ModelSerializer):
#     """
#     用户序列化类
#     """
#     username    = serializers.CharField(required=False, read_only=False, max_length=32, label="用户名", help_text="用户名")
#     name        = serializers.CharField(required=False, read_only=False, label="姓名", help_text="姓名")
#     is_active   = serializers.BooleanField(required=False, label="登陆状态", help_text="登陆状态")
#     email       = serializers.CharField(read_only=True, help_text="联系邮箱")
#     last_login  = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True, help_text="上次登录时间")
#     phone       = serializers.CharField(required=False, max_length=11, min_length=11, allow_null=True, help_text="手机号",
#                                         error_messages={"max_length":"手机号错误","min_length":"手机号错误"},
#                                         )
#
#     class Meta:
#         model = User
#         fields = ("id", "username", "name", "phone", "email", "is_active", "last_login")
#




# 支持用户注册,post请求; 还支持修改密码
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
        attrs["is_active"] = False
        attrs["email"] = "{}{}".format(attrs['username'], settings.DOMAIN)
        return attrs

    def create(self, validated_data):
        instance = super(UserRegSerializer, self).create(validated_data=validated_data)
        instance.set_password(validated_data["password"])
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
        # 最终修改是在这个地方
        password = validated_data.get("password", None)
        if password:
            instance.set_password(password)
            instance.save()
        return instance



# class UserRegSerializer(serializers.ModelSerializer):
#     """
#     用户注册序列化类
#     """
#     id       = serializers.IntegerField(read_only=True)
#     name     = serializers.CharField(max_length=32, label="姓名", help_text="用户姓名，中文姓名")
#     username = serializers.CharField(max_length=32, label="用户名", help_text="用户名，用户登陆名")
#     password = serializers.CharField(style={"input_type": "password"}, label="密码", write_only=True, help_text="密码")
#     phone    = serializers.CharField(max_length=11, min_length=11, label="手机号", required=False,
#                                      allow_null=True, allow_blank=True, help_text="手机号")
#
#     def create(self, validated_data):
#         validated_data["is_active"] = False
#         instance = super(UserRegSerializer, self).create(validated_data=validated_data)
#         instance.email = "{}{}".format(instance.username, settings.DOMAIN)
#
#         instance.set_password(validated_data["password"])
#         instance.id_rsa_key, instance.id_rsa_pub = self.get_sshkey(instance.email)
#         instance.save()
#         return instance
#
#     def update(self, instance, validated_data):
#         password =  validated_data.get("password", None)
#         if password:
#             instance.set_password(password)
#             instance.save()
#         return instance
#
#     def get_sshkey(self, email):
#         output = io.StringIO()
#         sbuffer = io.StringIO()
#
#         key = RSAKey.generate(2048)
#         key.write_private_key(output)
#         private_key = output.getvalue()
#
#         sbuffer.write("{} {} {}".format(key.get_name(), key.get_base64(), email))
#         public_key = sbuffer.getvalue()
#         return private_key, public_key
#
#     class Meta:
#         model = User
#         fields = ("username", "password", "name", "id", "phone")
