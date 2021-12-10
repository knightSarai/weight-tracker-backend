from django.urls import path

from . import views

app_name = "trainees"

urlpatterns = [
    path('measurements/', views.WeightMeasurementList.as_view(), name="allusermeasurements"),
]
