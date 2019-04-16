#!/usr/bin/python
#coding:utf-8

from django.core.management.base import BaseCommand
from resources.apscheduler import scheduler

class Command(BaseCommand):
    help = "django schedule"
    def handle(self, *args, **options):
        scheduler.start()

