from django.urls import path

from . import views

app_name = "trainees"

urlpatterns = [
    path('measurements/', views.WeightMeasurementList.as_view(), name="allmusermeasurements"),
    path('measurements/<int:pk>/', views.WeightMeasurementDetail.as_view(), name="measurementdetail"),
]
