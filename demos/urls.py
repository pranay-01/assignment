from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import formview ,Autoview, Auto_send

router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('rest-auth/', include('rest_auth.urls')),
    path('csrf/', formview),
    path('auto/', Autoview),
    path('auto_send/', Auto_send, name= 'auto_send'),
]