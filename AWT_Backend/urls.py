from django.urls import path, include
from django.contrib.auth.models import User
from django.contrib import admin
from rest_framework import routers, serializers, viewsets, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Anti wandering Tracker Device for autistic children",
      default_version='v1',
      description="Device for monitoring autistic children when they wander",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="angelnagaba9@gmail.com"),
      license=openapi.License(name="Private"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    #path('', include(router.urls)),
    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('caretaker/', include('caretaker.urls', namespace="caretaker_api")),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


]