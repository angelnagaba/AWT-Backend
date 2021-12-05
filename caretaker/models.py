from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim
import phonenumbers
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.gis.db import models
from geopy.geocoders import Nominatim
# Create your models here.



class AutisticChildren(models.Model):
    #child = models.OneToOneField(User, on_delete=models.CASCADE, related_name='child')
    child_name = models.CharField(max_length=100, null=False, blank=False)
    caretaker = models.ForeignKey('Care_taker', on_delete=models.CASCADE, null=True, blank=True, related_name='caretaker')
    AWT_device = models.ForeignKey('AWT_Device', on_delete=models.CASCADE, related_name='device', null=True, blank=True)
    Emergency_contact_name = models.CharField(max_length=100, null=False, blank=False)
    Emergency_contact_phone = PhoneNumberField(_('Phone number'), blank=False, null=True)
    Emergency_contact_address = models.CharField(max_length=100, null=False, blank=False)

class Care_taker(models.Model):

    caretaker_name = models.CharField(max_length=100, null=False, blank=False)
    child = models.ForeignKey('AutisticChildren', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    location = models.PointField(srid=4326, null=True)
    contact = PhoneNumberField(_('Phone number'), blank=False, null=True)

    def __str__(self):
        return self.caretaker_name

    @property
    def compute_location(self):
        geolocator = Nominatim(user_agent="caretaker", timeout=10)

        try:
            lat = str(self.location.y)
            lon = str(self.location.x)
            location = geolocator.reverse(lat + "," + lon)
            return '{}'.format(location.address)
        except:
            # location = str(self.location.y) + "," + str(self.location.x)
            return 'slow network, loading location ...'

class AWT_Device(models.Model):
    serial_no = models.CharField(max_length=100, null=False, blank=False)
