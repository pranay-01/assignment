from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ManufacturerViewset, DisplayPlaceViewset, CarViewset, BikeViewset, CustomViewset, MultiViewset

router = DefaultRouter()

router.register(r'manufacturers', ManufacturerViewset)
router.register(r'displayplaces', DisplayPlaceViewset)
router.register(r'bikes', BikeViewset)
router.register(r'cars', CarViewset)
router.register(r'customs', CustomViewset)
router.register(r'multiple', MultiViewset, basename= 'multiple')



urlpatterns = [
    path('', include(router.urls)),
    path('rest-auth/', include('rest_auth.urls')),
]