from django.urls import include, path
from rest_framework import routers
from . views import (CaretakerViewSet,ChildViewSet, DeviceViewSet)
from rest_framework.urlpatterns import format_suffix_patterns


router = routers.DefaultRouter()
router.register(r'caretakers', CaretakerViewSet, basename='caretaker')
router.register(r'children', ChildViewSet, basename='child')
router.register(r'devices', DeviceViewSet, basename='device')


app_name = 'caretaker'
urlpatterns = [
    path('api/', include(router.urls)),

]