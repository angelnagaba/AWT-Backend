from django.urls import include, path
from rest_framework import routers
from . views import (CaretakerViewSet,ChildViewSet, DeviceViewSet, UserViewSet, LoginAPI)
from rest_framework.urlpatterns import format_suffix_patterns
from knox import views as knox_views

router = routers.DefaultRouter()
#router.register(r'caretakers', CaretakerViewSet, basename='caretaker')
router.register(r'children', ChildViewSet, basename='child')
router.register(r'devices', DeviceViewSet, basename='device')
router.register(r'users',UserViewSet, basename='users')
#router.register(r'login',LoginAPI, basename='login')



app_name = 'caretaker'
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
]

