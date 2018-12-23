# -*- coding: utf-8 -*-


from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.conf import settings
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化类
    """
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                            label="上次登录时间",
                                            help_text="上次登录时间")

    class Meta:
        model = User
        fields = ("id", "username", "name", "phone", "email", "is_active", "last_login")


    def update(self, instance, validated_data):
        instance.phone = validated_data.get("phone", instance.phone)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        return instance


class UserRegSerializer(serializers.ModelSerializer):
    """
    用户注册序列化类
    """
    password = serializers.CharField(style={"input_type": "password"},
                                     label="密码",
                                     write_only=True,
                                     help_text="密码")
    def validate(self, attrs):
        attrs["is_active"] = False
        attrs["email"] = "{}{}".format(attrs['username'], settings.DOMAIN)
        return attrs

    def create(self, validated_data):
        instance = super(UserRegSerializer, self).create(validated_data=validated_data)
        instance.set_password(validated_data["password"])
        instance.save()
        return instance

    def update(self, instance, validated_data):
        # 最终修改是在这个地方
        password = validated_data.get("password", None)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

    class Meta:
        model = User
        fields = ("username", "password", "name", "id", "phone")

