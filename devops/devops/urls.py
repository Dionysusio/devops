from django.conf.urls import url,include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from idcs.views import IdcListViewset
from users.views import UserViewset
from cabinet.views import CabinetViewset
from manufacturer.views import ManufacturerViewset,ProductModelViewset
from servers.views import ServerAutoReportViewset,ServerViewset,NetworkDeviceViewset


route = DefaultRouter()
route.register("idcs",IdcListViewset,base_name="idcs")
route.register("users",UserViewset,base_name="users")
route.register("cabinet",CabinetViewset,base_name="cabinet")
route.register("manufacturer",ManufacturerViewset,base_name="manufacturer")
route.register("productmodel",ProductModelViewset,base_name="productmodel")
route.register("ServerAutoReport",ServerAutoReportViewset,base_name="ServerAutoReport")
route.register("servers",ServerViewset,base_name="servers")
route.register("networkdevice",NetworkDeviceViewset,base_name="networkdevice")

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^', include("idcs.urls")),  以后这个文件不需要了,甚至admin也不需要
    url(r'^', include(route.urls)),
    url(r'^docs/',include_docs_urls("little amy运维平台接口文档"))

]
