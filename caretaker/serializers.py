from rest_framework import serializers
from .models import (Care_taker, AutisticChildren)
from django.contrib.auth.models import User
from drf_extra_fields.fields import Base64ImageField
from geopy.geocoders import Nominatim
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CaretakerSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Care_taker
        fields = [ 'id','location','contact','home_address']

    
class ChildSerializer(serializers.ModelSerializer):
    caretaker= serializers.ReadOnlyField(source='caretaker.user.username')

    class Meta:
        model = AutisticChildren
        fields = ['id', 'child_name','caretaker','AWT_device_serialNo','Emergency_contact_name', 'Emergency_contact_phone','Emergency_contact_address']


#User Serializer
class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    is_active= serializers.BooleanField()
    username = serializers.CharField(max_length=200,required=True)
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
        
            instance.caretaker.contact = caretaker_data['contact']
            instance.caretaker.home_address = caretaker_data['home_address']
            instance.caretaker.location = caretaker_data['location']
            # And save caretaker
            instance.caretaker.save()
        # Rest will be handled by DRF
        return super().update(instance, validated_data)



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    caretaker = None

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token
    
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)

        # Custom data you want to include
        data.update({'user': self.user.username})
        data.update({'id': self.user.id})
        data.update({'first name': self.user.first_name})
        data.update({'last name': self.user.last_name})
        data.update({'email': self.user.email})
        try:
            data.update({'location': str(self.user.caretaker.location)})        
            data.update({'contact': str(self.user.caretaker.contact)})
            data.update({'home_address': self.user.caretaker.home_address})
            
        except:
            caretaker = None
        
        return data