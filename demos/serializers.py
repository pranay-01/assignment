from rest_framework import  serializers
from .models import Bank, Sample, DemoModel, FileUpload



class BankSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bank
        fields = '__all__'

class SampleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sample
        fields = '__all__'

class DemoModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = DemoModel
        fields = '__all__'


class FileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model= FileUpload
        fields = '__all__'