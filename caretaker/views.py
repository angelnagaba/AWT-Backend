from django.shortcuts import render
from .models import (Care_taker,AutisticChildren, AWT_Device)
from .serializers import (CaretakerSerializer, ChildSerializer, DeviceSerializer)
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.urls import reverse_lazy
from django.http import (HttpResponseRedirect, JsonResponse, HttpResponse,
                         Http404)
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView, ListView)
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import datetime
from django.db import IntegrityError
#from django_postgres_extensions.models.expressions import Index, SliceArray
#from rest_framework import filters
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
# views for sector


class CaretakerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sectors to be viewed or edited.
    """
    queryset = Care_taker.objects.all().order_by('-id')
    serializer_class = CaretakerSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChildViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sectors to be viewed or edited.
    """
    queryset = AutisticChildren.objects.all().order_by('-id')
    serializer_class = ChildSerializer
    permission_classes = [permissions.IsAuthenticated]


class DeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sectors to be viewed or edited.
    """
    queryset = AWT_Device.objects.all().order_by('-id')
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]
