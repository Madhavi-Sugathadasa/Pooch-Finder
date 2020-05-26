from django.contrib import admin
from .models import Breed, Dog_Type, Age_Cat, Gender, Picture, Location, Ad_Item, State

# Register your models here.
admin.site.register(Breed)
admin.site.register(Dog_Type)
admin.site.register(Age_Cat)
admin.site.register(Gender)
admin.site.register(Picture)
admin.site.register(Location)
admin.site.register(Ad_Item)
admin.site.register(State)