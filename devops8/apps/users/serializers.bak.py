# -*- coding: utf-8 -*-


from rest_framework import serializers
from django.contrib.auth.models import Group

from django.contrib.auth import get_user_model
from django.conf import settings
User = get_user_model()



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # fields = "__all__"
        exclude = ("password","groups","user_permissions")
        #这些字段不要,不显示


    def update(self, instance, validated_data):
        instance.phone = validated_data.get("phone",instance.phone)
        instance.is_active = validated_data.get("is_active",instance.is_active)
        return instance

