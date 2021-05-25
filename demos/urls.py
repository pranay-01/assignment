from django.urls import path, include
from .views import (Formview,
                    Autoview,
                    Auto_send,
                    SampleView,
                    SimpleUpload,
                    UploadView,
                    Example,
                    ScenarioFour,
                    ScenarioFive,
                    ScenarioTen,
                    ScenarioNine,

                    )

urlpatterns = [

    path('rest-auth/', include('rest_auth.urls')),
    path('csrf/', Formview),
    path('auto/', Autoview),
    path('auto_send/', Auto_send, name='auto_send'),
    path('upload/', SimpleUpload),
    path('upload64/', UploadView.as_view()),
    path('sample/', SampleView.as_view()),
    path('example/', Example.as_view()),
    path('scenario4/', ScenarioFour.as_view()),
    path('scenario5/', ScenarioFive.as_view()),
    path('scenario9/', ScenarioNine.as_view()),
    path('scenario10/', ScenarioTen.as_view()),


]