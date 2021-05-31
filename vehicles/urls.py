from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path, include
from .views import (Simple,
                    ManufacturerViewset,
                    OwnerViewset,
                    DisplayPlaceViewset,
                    CarViewset,
                    BikeViewset,
                    CustomViewset,
                    MultiViewset,
                    MultiCreate,
                    SleepView,
                    ScenarioOne,
                    ScenarioThree,
                    ScenarioTwo,
                    ScenarioSix,
                    ScenarioSeven,
                    ScenarioEleven,
                    ScenarioEight,
                    )

router = DefaultRouter()
route = SimpleRouter()

router.register(r'simple', Simple)
router.register(r'owners', OwnerViewset)
router.register(r'manufacturers', ManufacturerViewset)
router.register(r'displayplaces', DisplayPlaceViewset)
router.register(r'bikes', BikeViewset)
router.register(r'cars', CarViewset)
router.register(r'customs', CustomViewset)
router.register(r'multiple', MultiViewset, basename= 'multiple')
route.register(r'scenario11', ScenarioEleven, basename='scenario11')




urlpatterns = [
    path('', include(router.urls)),
    path('', include(route.urls)),
    path('rest-auth/', include('rest_auth.urls')),
    path('multi/',  MultiCreate),
    path('sleep/', SleepView.as_view()),
    path('scenario1/', ScenarioOne.as_view()),
    path('scenario2/', ScenarioTwo.as_view()),
    path('scenario3/', ScenarioThree.as_view()),
    path('scenario6/', ScenarioSix.as_view()),
    path('scenario7/', ScenarioSeven.as_view()),
    path('scenario8/', ScenarioEight.as_view()),

]