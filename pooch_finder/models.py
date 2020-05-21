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