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