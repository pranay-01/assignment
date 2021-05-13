from django.contrib import admin
from .models import Manufacturer, DisplayPlace, Car, Bike, Custom

admin.site.register(Manufacturer)
admin.site.register(DisplayPlace)
admin.site.register(Car)
admin.site.register(Bike)
admin.site.register(Custom)