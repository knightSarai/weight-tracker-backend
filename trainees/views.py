from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import permissions, generics

from .permissions import WeightMeasurementPermission
from .serializers import WeightMeasurementSerializer


@method_decorator(csrf_protect, name="dispatch")
class WeightMeasurementList(generics.ListCreateAPIView, WeightMeasurementPermission):
    permission_classes = [permissions.IsAuthenticated, WeightMeasurementPermission]
    serializer_class = WeightMeasurementSerializer

    def get_queryset(self):
        user = self.request.user
        return user.trainee.all_measurements


class WeightMeasurementDetail(generics.RetrieveUpdateDestroyAPIView, WeightMeasurementPermission):
    permission_classes = [permissions.IsAuthenticated, WeightMeasurementPermission]
    serializer_class = WeightMeasurementSerializer

    def get_queryset(self):
        user = self.request.user
        return user.trainee.all_measurements
