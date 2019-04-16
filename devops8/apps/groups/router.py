# -*- coding: utf-8 -*-

from rest_framework.routers import DefaultRouter
from .views import GroupViewset, UserGroupsViewset, GroupMembersViewset

group_router = DefaultRouter()

group_router.register('groups', GroupViewset, base_name="groups")
group_router.register('userGroups', UserGroupsViewset, base_name="userGroups")
group_router.register('groupMembers', GroupMembersViewset, base_name="groupMembers")


