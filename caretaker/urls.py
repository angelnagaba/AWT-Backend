from django.urls import include, path
from rest_framework import routers
from . views import (CaretakerViewSet,ChildViewSet, UserViewSet, MyObtainTokenPairView)
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.DefaultRouter()
router.register(r'children', ChildViewSet, basename='child')
router.register(r'caretakers',UserViewSet, basename='users')

app_name = 'caretaker'
urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

