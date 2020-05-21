from django.db import models
from django.contrib.auth.models import User
from django.conf import settings as conf_settings
from datetime import datetime 


# Create your models here.
class Breed(models.Model):
    name = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.name}"
    
class Dog_Type(models.Model):
    name = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.name}"
    
class Age_Cat(models.Model):
    name = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.name}"
    
class Gender(models.Model):
    name = models.CharField(max_length=8)
    
    def __str__(self):
        return f"{self.name}"
    
class Location(models.Model):
    postcode = models.CharField(max_length=8)
    suburb = models.CharField(max_length=20)
    state = models.CharField(max_length=5)
    lon = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.suburb}, {self.state}, {self.postcode}"
    
class State(models.Model):
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return f"{self.name}, {self.code}"
    
class Ad_Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ad_user")
    price = models.FloatField()
    negotiable = models.BooleanField(default=False)
    title = models.CharField(max_length=200)
    summary_desc = models.CharField(max_length=1000)
    desc = models.CharField(max_length=4000)
    gender = models.ForeignKey(Gender, on_delete=models.DO_NOTHING, related_name="ad_gender")
    age = models.ForeignKey(Age_Cat, on_delete=models.DO_NOTHING, related_name="ad_age")
    breed = models.ForeignKey(Breed, on_delete=models.DO_NOTHING, related_name="ad_breed")
    dog_type = models.ForeignKey(Dog_Type, on_delete=models.DO_NOTHING, related_name="ad_type")
    microchip_number =  models.CharField(max_length=200, null=True, blank=True)
    breeder_id = models.CharField(max_length=200, null=True, blank=True)
    contact_name = models.CharField(max_length=64, default="")
    email = models.CharField(max_length=64, default="")
    mobile = models.CharField(max_length=64, default="")
    item_location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, related_name="ad_location", default="")
    date_time = models.DateTimeField(default=datetime.now())
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.id} - {self.title}"
    
def photo_path_(instance, filename):
    return (conf_settings.MEDIA_PATH+'/{0}/{1}').format(instance.ad_item.id, filename)

class Picture(models.Model):
    ad_item = models.ForeignKey(Ad_Item, on_delete=models.CASCADE, related_name="ad_item")
    image = models.ImageField(upload_to = photo_path_)
    
    def __str__(self):
        return f"{self.image}"