#!/usr/bin/python
#coding:utf-8

from rest_framework.permissions import DjangoModelPermissions


class Permissions(DjangoModelPermissions):


    def get_custom_perms(self,view,method):
        #获取view里的extra_perm_map中的get属性
        if hasattr(view,"extra_perm_map"): #如果有属性
            if isinstance(view.extra_perm_map,dict): #如果是字典
                return view.extra_perm_map.get(method,[]) #返回属性的方法
        return []


    def has_permission(self, request, view):
        if getattr(view, '_ignore_model_permissions', False):
            return True

        if not request.user or (
           not request.user.is_authenticated and self.authenticated_users_only):
            return False

        queryset = self._queryset(view)
        perms = self.get_required_permissions(request.method, queryset.model)
        perms.extend(self.get_custom_perms(view,request.method)) #调用,2个列表相加
        print(perms) #增加
        return request.user.has_perms(perms)


