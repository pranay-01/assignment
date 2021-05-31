from rest_framework import  serializers
from django.contrib.auth.models import User
from .models import Manufacturer, DisplayPlace, Car, Bike, Custom


class OwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'car_set', 'bike_set')

class DisplayPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisplayPlace
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    class Meta:
        model = Car
        fields = '__all__'

class BikeSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Bike
        fields = '__all__'

    def validate_gears(self, value):

        if(value>6):
            raise serializers.ValidationError('Bike with these many gears does not exist')
        return value


class ManufacturerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manufacturer
        fields = '__all__'


class CustomSerializer(serializers.ModelSerializer):

    inspired_from = serializers.CharField(source='inspired.model_name', read_only=True)
    class Meta:
        model = Custom
        fields = '__all__'




#--------------Serializers for ORM----------------#

class OnlySerializer(serializers.ModelSerializer):
    class Meta:
        model= Manufacturer
        fields= ('id',)

class DeferSerializer(serializers.ModelSerializer):
  class Meta:
      model= Manufacturer
      fields= ('name','origin', 'created', 'modified')
