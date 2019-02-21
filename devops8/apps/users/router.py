# -*- coding: utf-8 -*-

from rest_framework.routers import DefaultRouter
from .views import UserViewset, UserRegViewset, UserInfoViewset


router = DefaultRouter()

router.register("Users", UserViewset, base_name="Users")
router.register("userReg", UserRegViewset, base_name="userReg")
router.register("UserInfo", UserInfoViewset, base_name="UserInfo")

