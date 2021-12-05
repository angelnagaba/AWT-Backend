from django.shortcuts import render

# Create your views here.
from rest_framework.generics import UpdateAPIView
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView)
from django.http import (HttpResponseRedirect, JsonResponse, HttpResponse,
                         Http404)
#from .forms import LoginForm, SignUpForm, PasswordResetEmailForm, UserForm, GroupForm, ProfileForm, UserUpdateForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.utils.encoding import force_text
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.urls import reverse_lazy
from .models import (Profile)
from django.core.mail import EmailMessage
from django.contrib.auth.views import PasswordResetView
from rest_framework.views import APIView
from rest_framework import parsers, renderers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework import permissions
#from .forms import ProfileForm
#from farmer.views import FarmerProfile
from django.db.models import Count, Q, Sum, FloatField
import json
from .serializers import (GroupSerializer, UserProfileSerializer, UserPostSerializer, UserApiPost, ProfileSerializer, UserSerializer)
from rest_framework import filters
from django.core import serializers as django_serializers
from rest_framework import status
from django.contrib.auth.forms import PasswordChangeForm
#from farm .models import Sector
from django.db.models.functions import Cast
from smtplib import SMTPException
#from django_rest_passwordreset.models import ResetPasswordToken
#from django_rest_passwordreset.views import get_password_reset_token_expiry_time
from django.utils import timezone
from datetime import timedelta
from rest_framework.generics import GenericAPIView
#from django_rest_passwordreset.serializers import EmailSerializer, PasswordTokenSerializer

from rest_framework.permissions import IsAuthenticated
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ValidationError
from rest_framework import status, exceptions
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.exceptions import ValidationError
#from django_rest_passwordreset.signals import reset_password_token_created, pre_password_reset, post_password_reset
from django.contrib.auth.password_validation import validate_password, get_password_validators
#from django_rest_passwordreset.signals import reset_password_token_created
#from django_rest_passwordreset.models import ResetPasswordToken, clear_expired, get_password_reset_token_expiry_time, \
    #get_password_reset_lookup_field
HTTP_USER_AGENT_HEADER = getattr(
    settings, 'DJANGO_REST_PASSWORDRESET_HTTP_USER_AGENT_HEADER', 'HTTP_USER_AGENT')
HTTP_IP_ADDRESS_HEADER = getattr(
    settings, 'DJANGO_REST_PASSWORDRESET_IP_ADDRESS_HEADER', 'REMOTE_ADDR')



class UserViewSet(viewsets.ModelViewSet):
    '''
    Interface for User registration
    '''

    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name',
                     'email','profile__phone_number']
    ordering_fields = '__all__'

    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer
        else:
            return UserPostSerializer
        return UserSerializer

    def get_queryset(self):
        users = User.objects.order_by('-id')
        user = self.request.user
        phone = self.request.query_params.get('phone_number', None)
        if phone is not None:
            queryset = queryset.filter(phone_number=phone)
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Admin').exists() or self.request.user.groups.filter(name='Data Entrant').exists():
            queryset = users
        else:
            queryset = User.objects.filter(id=user.id)

        return queryset

    def create(self, request, format=None):
        serializer = UserPostSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer
            user.save()

            # send an email
            # try:
            #     user_object = User.objects.get(
            #         username=serializer.data['username'])
            #     current_site = get_current_site(request)
            #     subject = 'Activate Your Account'
            #     message = render_to_string('account_activation_email.html', {
            #         'user': user_object,
            #         'domain': current_site.domain,
            #         'uid': urlsafe_base64_encode(force_bytes(user_object.id)),
            #         'token': account_activation_token.make_token(user_object),
            #     })
            #     to_email = serializer.data['email']
            #     email = EmailMessage(
            #         subject, message, to=[to_email]
            #     )

            #     email.send()
            # except SMTPException as e:
            #     print('There was an error sending an email: ', e)
            # response = {
            #     'status': 'Your account has been created successfully, please check your email to activate.'}
            # return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, format=None):
        instance = User.objects.get(pk=pk)
        serializer = UserProfileSerializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'profile updated successfully'})
        return Response({'error': serializer.errors}, status=400)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class PostUserDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows farms to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserApiPost
    permission_classes = [permissions.IsAuthenticated]


class PostProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
