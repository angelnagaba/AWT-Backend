from django.urls import include, path
from rest_framework import routers
from . views import (UserViewSet,PostUserDataViewSet, PostProfileViewSet)
from rest_framework.urlpatterns import format_suffix_patterns


router = routers.DefaultRouter()
router.register(r'register', UserViewSet, 'users')
# router.register(r'groups', views.GroupViewSet, 'groups')
router.register(r'post_users', PostUserDataViewSet, 'post_users')
router.register(r'profiles', PostProfileViewSet, 'profiles')

app_name = 'common'
urlpatterns = [
    path('api/', include(router.urls)),

]