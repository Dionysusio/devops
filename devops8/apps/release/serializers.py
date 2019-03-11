#!/usr/bin/python
#coding:utf-8

from rest_framework import serializers
from .models import Deploy
from django.contrib.auth import get_user_model
User = get_user_model()


class DeploySerializer(serializers.ModelSerializer):
    """ 工单列化类 """
    applicant = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # apply_time = serializers.DateTimeField(format="%Y-%m-$d %H:%M:%S", read_only=True)
    # complete_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Deploy
        fields = "__all__"

    def to_representation(self, instance):
        applicant_obj = instance.applicant
        reviewer_obj = instance.reviewer
        assign_to_obj = instance.assign_to
        status_value = instance.get_status_display()
        ret = super(DeploySerializer, self).to_representation(instance)
        ret['status'] = {
            "id": instance.status,
            "name": status_value
        }
        ret["applicant"] = {
            "id": applicant_obj.id,
            "name": applicant_obj.name
        }
        ret["reviewer"] = {
            "id": reviewer_obj.id,
            "name": reviewer_obj.name
        }
        if assign_to_obj:
            ret['assign_to'] = {
                "id": assign_to_obj.id,
                "name":assign_to_obj.username
            }

        return ret



