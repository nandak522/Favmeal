from django.db import models

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True        

class AddressManager(models.Manager):
    def create_address(self, place, landmark, area, city='Hyderabad', zip=None, latitude=None, longitude=None):
        address_exists = self.exists(place=place, landmark=landmark, area=area, city=city, zip=zip, latitude=latitude, longitude=longitude)
        if address_exists:
            return self.filter(place=place.strip().lower(), landmark=landmark.strip().lower(), area=area.strip().lower(), city=city, zip=zip, latitude=latitude, longitude=longitude)[0]
        address = Address(place=place, landmark=landmark, area=area, city=city, zip=zip, latitude=latitude, longitude=longitude)
        address.save()
        return address
    
    def exists(self, place, landmark, area, city='Hyderabad', zip=None, latitude=None, longitude=None):
        try:
            if self.filter(place=place.strip().lower(), landmark=landmark.strip().lower(), area=area.strip().lower(), city=city, zip=zip, latitude=latitude, longitude=longitude).count():
                return True
        except Address.DoesNotExist:
            return False
        return False

class Address(BaseModel):
    place = models.CharField(max_length=100, blank=False)
    landmark = models.CharField(max_length=50, blank=False)
    area = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, default='Hyderabad', blank=False)
    zip = models.IntegerField(max_length=6, blank=True, null=True)
    latitude = models.DecimalField(max_digits=17, decimal_places=14, blank=True, null=True)
    longitude = models.DecimalField(max_digits=17, decimal_places=14, blank=True, null=True)
    objects = AddressManager()

    def __unicode__(self):
        return '%s, %s' % (self.place, self.area)

