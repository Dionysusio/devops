#!/usr/bin/python
#coding:utf-8

from django_apscheduler.jobstores import DjangoJobStore,register_events,register_job
# from apscheduler.schedulers.background import BackgroundScheduler #后台运行
from apscheduler.schedulers.blocking import BlockingScheduler #前台运行
import datetime
from resources.qcloud.cvm import getCvmList

# scheduler = BackgroundScheduler()
scheduler = BlockingScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')


@register_job(scheduler,'interval',seconds=10)
def sync_cloud():
    print('my_scheduler is run:  {}'.format(datetime.datetime.now()))
    getCvmList() #采集腾讯云

register_events(scheduler)
# scheduler.start()


