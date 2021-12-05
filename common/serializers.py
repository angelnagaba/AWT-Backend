from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Profile
from django.contrib.auth.models import Group as UserGroup
from rest_framework.authtoken.models import Token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from drf_extra_fields.fields import Base64ImageField
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name')
    name = serializers.CharField()


    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    user_permissions = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name')
    groups = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)
    full_name = serializers.SerializerMethodField(
        method_name='get_user_full_name', source='username')
    phone_number = serializers.CharField(source='profile.phone_number')
    #gender = serializers.CharField(source='profile.get_gender_display')
    home_address = serializers.CharField(source='profile.home_address')
    
   

    def get_user_full_name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)
    
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
   

    class Meta:
        model = Profile
        fields = '__all__'


class UserPostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=200,required=True)
    first_name = serializers.CharField(max_length=200,required=True)
    last_name = serializers.CharField(max_length=200,required=True)
    email = serializers.EmailField(required=False, allow_null=True,allow_blank=True)
    #password = serializers.CharField(required=True, max_length=20)
    #profile = ProfileSerializer()
    

    def validate_email(self, value):
        try:
            lower_email = value.lower()
        except:
            lower_email = None
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("User already exists with this email.")
        return lower_email


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'is_active')

    def create(self, validated_data):

        # create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            #password=validated_data['password'],
            is_active=False
        )

        #profile_data = validated_data.pop('profile')

        # create profile
        profile = Profile.objects.create(
            user=user,
            #phone_number=profile_data['phone_number'],
            #phone_2=profile_data['phone_2'],
            #home_address=profile_data['home_address'],
            
        )
        #Token.objects.get_or_create(user=user)

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    # def update(self,instance, validated_data):
    #     if validated_data.get('profile'):
    #         profile_data = validated_data.pop('profile')
    #         profile_serializer = ProfileSerializer(data=profile_data)

    #         if profile_serializer.is_valid():
    #             profile = profile_serializer.update(instance = instance.profile)
    #             validated_data['profile'] = profile
    #     return super(UserProfileSerializer, self).update(instance, validated_data)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'profile','password')
   
class UserApiPost(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username','profile','password']
