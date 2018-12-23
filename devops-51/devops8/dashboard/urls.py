#!/usr/bin/python3
#coding:utf-8

from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^hello/', views.index,name='index'),
    # url(r'^login/$',views.loginView,name='loginView'),
    # url(r'^loginView/$',views.loginView.as_view()),
    url(r'^login/$',views.LoginVeiw.as_view()),
    url(r'^groupmembers/$',views.GroupMembersView.as_view()),
    url(r'^usergroups/$',views.UserGroupsView.as_view()),
    url(r'^usergroupmanage/$',views.UserGroupManageView.as_view()),

]

