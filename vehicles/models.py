from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.core.exceptions import ValidationError


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

@receiver(post_save, sender= DisplayPlace)
def show_mesg(sender, **kwargs):
    if kwargs['created']:
        print('New Place Added')


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


    def clean(self):
        if(self.gears > 6):
            raise ValidationError("Bike with these many gears does not exist")

    def save(self, *args, **kwargs):
        self.full_clean()

        super(Bike, self).save(*args, **kwargs)


class Custom(Vehicle):
    inspired = models.ForeignKey(Car, on_delete=models.CASCADE)




@receiver(post_save,  sender= DisplayPlace)
@receiver(post_save,  sender= Manufacturer)
@receiver(post_save, sender= Custom)
@receiver(post_delete, sender= DisplayPlace)
@receiver(post_delete, sender= Manufacturer)
@receiver(post_delete, sender= Custom)
def clear_cache(sender, instance, **kwargs):
    cache.clear()




class Place(models.Model):
    name = models.CharField(max_length=20)
    star = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

class Restaurant(Place):

    serve_pizza = models.BooleanField(default=False)
    serve_noodles = models.BooleanField(default=False)

    def __str__(self):
        return self.name