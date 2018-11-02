#!/usr/bin/python3
# coding:utf-8

import sys
import os
import django

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(project_dir)
# print(project_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devops.settings")
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()


def get_users():
    for user in User.objects.all():
        print(user.username)


if __name__ == "__main__":
    get_users()
