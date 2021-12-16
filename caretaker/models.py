
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim
import phonenumbers
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.gis.db import models
from geopy.geocoders import Nominatim

# Models here.
class AutisticChildren(models.Model):
    child_name = models.CharField(max_length=100, null=False, blank=False)
    caretaker = models.ForeignKey('Care_taker', on_delete=models.CASCADE, null=True, blank=True, related_name='caretaker')
    AWT_device_serialNo = models.CharField(max_length=100, null=True, blank=True)
    Emergency_contact_name = models.CharField(max_length=100, null=False, blank=False)
    Emergency_contact_phone = PhoneNumberField(_('Phone number'), blank=False, null=False)
    Emergency_contact_address = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.child_name


class Care_taker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='caretaker',default=1)
    location = models.PointField(srid=4326, null=True)
    contact = PhoneNumberField(_('Phone number'), blank=False, null=True)
    home_address = models.TextField(max_length=100, blank=True)

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

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

