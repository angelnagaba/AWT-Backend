from django.urls import path, include
from django.contrib.auth.models import User
from django.contrib import admin
from rest_framework import routers, serializers, viewsets


urlpatterns = [
    #path('', include(router.urls)),
    
    path('caretaker/', include('caretaker.urls', namespace="caretaker_api")),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', admin.site.urls),

]