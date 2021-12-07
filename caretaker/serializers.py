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
        fields = ['id', 'caretaker_name','child','location','contact']

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
