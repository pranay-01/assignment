from django.shortcuts import render
from rest_framework import permissions
from rest_framework import viewsets
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
from  .models import Manufacturer,DisplayPlace,Car,Bike, Custom
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import ManufacturerSerializer, DisplayPlaceSerializer, CarSerializer, BikeSerializer, CustomSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class ManufacturerViewset(viewsets.ModelViewSet):
    serializer_class = ManufacturerSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['name', 'origin', 'id']
    ordering_fields = ['name', 'origin','id']
    search_fields = ['name','origin','id']
    queryset = Manufacturer.objects.all()

class DisplayPlaceViewset(viewsets.ModelViewSet):
    serializer_class = DisplayPlaceSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['area', 'id']
    ordering_fields = ['area', 'id']
    search_fields = ['area', 'id']
    queryset = DisplayPlace.objects.all()


class CarViewset(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['model_name', 'model_num', 'color', 'gears', 'category', 'is_dct']
    ordering_fields = ['model_name', 'model_num', 'color', 'gears', 'category', 'is_dct']
    search_fields = ['model_name', 'model_num', 'color', 'gears', 'category', 'is_dct']
    queryset = Car.objects.all()

class BikeViewset(viewsets.ModelViewSet):
    serializer_class = BikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['model_name', 'model_num', 'color', 'gears', 'type', 'tubeless_tyres']
    ordering_fields = ['model_name', 'model_num', 'color', 'gears', 'type', 'tubeless_tyres']
    search_fields = ['model_name', 'model_num', 'color', 'gears', 'type', 'tubeless_tyres']
    queryset = Bike.objects.all()


class CustomViewset(viewsets.ModelViewSet):
    serializer_class = CustomSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['model_name', 'model_num', 'color', 'gears']
    ordering_fields = ['model_name', 'model_num', 'color', 'gears']
    search_fields = ['model_name', 'model_num', 'color', 'gears']
    queryset = Custom.objects.all()


class MultiViewset(ObjectMultipleModelAPIViewSet):

    querylist = [
        {
            'queryset': Manufacturer.objects.all(),
            'serializer_class': ManufacturerSerializer,
        },
        {
            'queryset': DisplayPlace.objects.all(),
            'serializer_class': DisplayPlaceSerializer,
        },
        {
            'queryset': Custom.objects.all(),
            'serializer_class': CustomSerializer,
        }
    ]

    @method_decorator(cache_page(CACHE_TTL))
    def dispatch(self, *args, **kwargs):
        return super(MultiViewset, self).dispatch(*args, **kwargs)
