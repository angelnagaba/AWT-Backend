from django.shortcuts import render
from .models import (Care_taker,AutisticChildren, AWT_Device)
from .serializers import (CaretakerSerializer, ChildSerializer, DeviceSerializer, UserSerializer, UserPostSerializer)
from rest_framework import viewsets, filters
from rest_framework import permissions, status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
#Login
from django.contrib.auth import authenticate
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse_lazy
from django.http import (HttpResponseRedirect, JsonResponse, HttpResponse,
                         Http404)
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView, ListView)
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
import datetime
from django.db import IntegrityError
#from django_postgres_extensions.models.expressions import Index, SliceArray
#from rest_framework import filters
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point

# views for login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView


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


class UserViewSet(viewsets.ModelViewSet):
    '''
    Interface for User registration
    '''

    serializer_class = UserPostSerializer
    queryset = User.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    search_fields = ['username', 'first_name', 'last_name',
                     'email']
    ordering_fields = '_all_'


    def create(self, request, format=None):
        serializer = UserPostSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer
            user.save()

            # send an email
            # user_object = User.objects.get(
            #     username=serializer.data['username'])
            # current_site = get_current_site(request)
            # subject = 'Activate Your Account'
            # message = render_to_string('account_activation_email.html', {
            #     'user': user_object,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user_object.id)),
            #     'token': account_activation_token.make_token(user_object),
            # })
            # to_email = serializer.data['email']
            # email = EmailMessage(
            #     subject, message, to=[
            #         to_email], from_email="musa@8technologies.net"
            # )
            # email.content_subtype = "html"
            # try:
            #     email.send()
            # except SMTPException as e:
            #     print('There was an error sending an email: ', e)
            response = {
                'response': 'Your caretaker account has been created successfully, Please register your child'}
            return Response(response, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):

        instance = User.objects.get(pk=kwargs.get('pk'))
        serializer = UserPostSerializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():

            serializer.save()
            return Response({'response': 'your caretaker profile has been updated successfully'})
        return Response({'response': serializer.errors}, status=400)

#Login view
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)