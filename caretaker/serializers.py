from rest_framework import serializers
from .models import (Care_taker, AutisticChildren, AWT_Device)

from django.contrib.auth.models import User
from drf_extra_fields.fields import Base64ImageField
from geopy.geocoders import Nominatim


class CaretakerSerializer(serializers.ModelSerializer):
    # caretaker_name = serializers.SlugRelatedField(many=True,read_only=True, slug_field='name')
    # location = serializers.SlugRelatedField(many=True,read_only=True, slug_field='location')
    # contact = serializers.SlugRelatedField(many=False,read_only=True, slug_field='contact')
   
    class Meta:
        model = Care_taker
        fields = [ 'user','location','contact','home_address']

    # def get_user_full_name(self, obj):
    #     return '{} {}'.format(obj.user.first_name, obj.user.last_name)

class ChildSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = AutisticChildren
        fields = ['id', 'child_name','caretaker','AWT_device','Emergency_contact_name']

    # def get_caretaker_name(self, obj):
    #     return '{} {}'.format(obj.)

#AWTDevice Serializer
class DeviceSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = AWT_Device
        fields = ['id', 'serial_no']


#User Serializer
class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    is_active= serializers.BooleanField()
    username = serializers.CharField(max_length=100)
    full_name = serializers.SerializerMethodField(
        method_name='get_user_full_name', source='username')
    contact = serializers.CharField(
        source='caretaker.contact', required=False,)
    home_address = serializers.CharField(source='caretaker.home_address')
    def get_user_full_name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)

    class Meta:
        model = User
        fields = '_all_'


#User post serializer
class UserPostSerializer(serializers.ModelSerializer):
    caretaker = CaretakerSerializer()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password', 'caretaker')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        # create user
        user = User.objects.create_user(
           
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name = validated_data['last_name'],
            password=validated_data['password'],
            username=validated_data['username'],
            is_active=True
        )
        caretaker_data = validated_data.pop('caretaker')
         # create caretaker
        caretaker = Care_taker.objects.create(
            user=user,
            contact=caretaker_data['contact'],
            home_address=caretaker_data['home_address'],
            location=caretaker_data['location'],
        )

        return user

    def update(self, instance, validated_data):
        # We try to get caretaker data
        caretaker_data = validated_data.pop('caretaker', None)
        # If we have one
        if caretaker_data is not None:
            instance.caretaker.phone_number = caretaker_data['phone_number']
            instance.caretaker.alternative_contact = caretaker_data['alternative_contact']
            instance.caretaker.gender = caretaker_data['gender']
            # And save caretaker
            instance.caretaker.save()
        # Rest will be handled by DRF
        return super().update(instance, validated_data)