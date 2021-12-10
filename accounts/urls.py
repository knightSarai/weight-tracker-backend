from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path('csrf/', views.GetCSRFToken.as_view(), name="api-csrf"),
]
