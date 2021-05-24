from django.shortcuts import render
from time import sleep
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, APIView
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db import transaction
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
from .models import Manufacturer,DisplayPlace,Car,Bike, Custom
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import OwnerSerializer, ManufacturerSerializer, DisplayPlaceSerializer, CarSerializer, BikeSerializer, CustomSerializer, OnlySerializer, DeferSerializer
from rest_framework.response import Response
from django.db.models import F
from django.db import connection

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)




class OwnerViewset(viewsets.ModelViewSet):
    serializer_class = OwnerSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['id', 'username']
    ordering_fields = ['id', 'username']
    search_fields = ['id', 'username']
    queryset = User.objects.all()

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
    queryset = Car.objects.select_related('owner').all()

class BikeViewset(viewsets.ModelViewSet):
    serializer_class = BikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['model_name', 'model_num', 'color', 'gears', 'type', 'tubeless_tyres']
    ordering_fields = ['model_name', 'model_num', 'color', 'gears', 'type', 'tubeless_tyres']
    search_fields = ['model_name', 'model_num', 'color', 'gears', 'type', 'tubeless_tyres']
    queryset = Bike.objects.select_related('owner').all()


class CustomViewset(viewsets.ModelViewSet):
    serializer_class = CustomSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['model_name', 'model_num', 'color', 'gears']
    ordering_fields = ['model_name', 'model_num', 'color', 'gears']
    search_fields = ['model_name', 'model_num', 'color', 'gears']
    queryset = Custom.objects.select_related('inspired').all()


#----------------------------------CACHING--------------------------------#

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


#-------------------------------------TRANSACTIONS------------------------------#

@transaction.atomic
@api_view(['GET','POST'])
def MultiCreate(request):
    d1=DisplayPlace.objects.get(area='Toronto')


    Manufacturer.objects.create(name='Ferrari', origin='Italy')
    Car.objects.create(model_name='Aventador', model_num='30', color='Orange', gears=6, category='supersport', owner=request.user, display=d1, is_dct=True)
    DisplayPlace.objects.create(area='Malaysia')
    Bike.objects.create(model_name='Ninja H2', model_num=22, color='Green', gears=6, type='supersport', owner=request.user, tubeless_tyres=True)

    return Response({"message" : "Creation Successful!"})


@transaction.atomic
@api_view(['GET', 'PUT'])
def SleepView(request, id):

    if id:
        t= Car.objects.get(id=id)
        print('Beginning Sleep   ' + t.model_name)
        sleep(10)
        print('Woke Up')
        t.gears = 8
        t.save()
        print(t.gears)
        return Response({'message' : 'Updated Successfully'})

    return Response({'message' : 'Invalid ID'})


# ___________________ORM VIEWS_____________________#


class ScenarioTwo(APIView):

    def get(self, request, format=None):
        mod_ids=[]
        mod_ids+=(Custom.objects.values_list(F('id')*100, flat=True))
        return Response([
            {'Message': 'Modified Ids for Custom Model'},
            {'Modified_ID': mod_ids}
        ])


class ScenarioThree(APIView):

    def get(self, request, format=None):
        ids=[]
        combine = []
        for each in Car.objects.all():
            combine.append({'id': each.id, 'Count Of Related Objects': each.custom_set.all().count()})

        return Response(combine)


class ScenarioSix(APIView):

    def get(self, request, format=None):

        for each in Car.objects.all():
            print(each.id,
                  each.custom_set.values_list('model_name'),
                  each.manufacturer.values_list('name'),
                  each.owner.username,
                  each.display.area)

        return Response({'Query Count': len(connection.queries)})


class ScenarioSeven(APIView):

    def get(self, request, format=None):

        for each in Car.objects.select_related('owner').prefetch_related('manufacturer', 'custom_set').all():
            print(each.id,
                  each.custom_set.all(),
                  each.manufacturer.values_list('name'),
                  each.owner.username,
                  each.display.area)

        return Response({'Query Count': len(connection.queries)})


class ScenarioEight(APIView):
    # Not implemented completely

    #serializer_class = OnlySerializer

    def get(self, request, format=None):
        only_list = Manufacturer.objects.only('id')
        ser1 = ManufacturerSerializer(only_list)
        serializer = OnlySerializer(only_list)
        #defer_list = Manufacturer.objects.defer('id')
        val = Manufacturer.objects.values('id')
        val_list = Manufacturer.objects.values_list('id', flat=True)

        return Response({
            "only_list": ser1.data,
            "values_list": val_list,
            "values": val,
        })


class ScenarioEleven(viewsets.ReadOnlyModelViewSet):


    def list(self, request, *args, **kwargs):
        disp_count = DisplayPlace.objects.count()
        data = {'Count of DisplayPlaces': disp_count}
        return Response(data)

    def retrieve(self, request, pk=None, *args, **kwargs):

        x = request.query_params.get('data')
        if DisplayPlace.objects.filter(id=pk).exists():

            if x == 'True':
                gt= DisplayPlace.objects.get(id=pk)
                serializer = DisplayPlaceSerializer(gt)
                return Response({'data': serializer.data})
            else:
                return Response({'mesg': 'Cannot Access'})
        else:

            return Response({'mesg': 'Invalid ID'})


