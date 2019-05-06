from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

# from groupUsers.views import GroupUserViewset
from users.router import router as user_router
from groups.router import group_router

from permissions.router import permission_router
# from resources.router import router as resources_router
from books.router import router as books_router
from workorder.router import workorder_router
from autotask.router import autotask_router
from release.router import deploy_router
# from kiwi.router import kiwi_router
# from resources import apscheduler



router = DefaultRouter()
# router.register("groupUsers", GroupUserViewset, base_name="groupUsers")
router.registry.extend(user_router.registry)
router.registry.extend(group_router.registry)

# router.registry.extend(resources_router.registry)
router.registry.extend(permission_router.registry)
router.registry.extend(books_router.registry)
router.registry.extend(workorder_router.registry)
router.registry.extend(autotask_router.registry)
router.registry.extend(deploy_router.registry)
# router.registry.extend(kiwi_router.registry)



urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^', include(router.urls)),
    url(r'^', include("projects.urls")),
    # url(r'^', include("kiwi.urls")),
    # url(r'^', include('resources.urls')),
    url(r'^api-auth', include('rest_framework.urls')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^docs/', include_docs_urls("friedrich运维接口平台文档")),

]



