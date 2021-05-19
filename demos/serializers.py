from rest_framework import  serializers
from .models import Bank, Sample

class BankSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bank
        fields = '__all__'

class SampleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sample
        fields = '__all__'
