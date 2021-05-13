from django.db import models
from django.contrib.auth.models import User


class AutoTime(models.Model):
    created = models.DateTimeField(auto_now_add=True, auto_now=False, blank=False)
    modified = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True


class Vehicle(AutoTime):
    model_name = models.CharField(max_length=50)
    model_num = models.PositiveSmallIntegerField()
    color = models.CharField(max_length=25)
    gears = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True
        ordering = ('id',)

    def __str__(self):
        return self.model_name


class Manufacturer(AutoTime):
    name = models.CharField(max_length=50, unique=True)
    origin = models.CharField(max_length=25)
    logo = models.ImageField(null=True, blank=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name

class DisplayPlace(AutoTime):
    area = models.CharField(max_length=50)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.area


class Car(Vehicle):
    CATEGORIES = (
        ('muscle', 'Muscle'),
        ('suv', 'SUV'),
        ('supersport', 'SUPER_SPORT'),
        ('convertible', 'CONVERTIBLE'),
        ('pickup', 'PICK_UP'),
        ('hatchback', 'HATCHBACK'),
        ('4x4offroad', '4X4_OFFROAD'),
    )
    category = models.CharField(max_length=20, choices=CATEGORIES, help_text='Choose from the list')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    manufacturer = models.ManyToManyField(Manufacturer)
    display = models.OneToOneField(DisplayPlace, on_delete=models.PROTECT)
    is_dct = models.BooleanField()


class Bike(Vehicle):
    TYPES = (
        ('adventure', 'ADV'),
        ('caferacer', 'CAFE_RACER'),
        ('supersport', 'SUPER_SPORT'),
        ('cruiser', 'CRUISER'),
        ('commuter', 'COMMUTER'),
        ('streetnaked', 'STREET_NAKED'),
        ('tourer', 'TOURER'),
    )
    type = models.CharField(max_length=15, choices=TYPES, help_text='Choose from the list')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    manufacturer = models.ManyToManyField(Manufacturer)
    tubeless_tyres = models.BooleanField()


class Custom(Vehicle):
    inspired = models.ForeignKey(Car, on_delete=models.CASCADE)
