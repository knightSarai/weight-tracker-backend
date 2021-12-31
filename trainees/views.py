from django.db import transaction
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from .models import Trainee, WeightMeasurement
from .permissions import WeightMeasurementPermission
from .serializers import WeightMeasurementSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class WeightMeasurementList(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [permissions.IsAuthenticated, WeightMeasurementPermission]

    @staticmethod
    def get(request):
        user = request.user

        if hasattr(user, 'trainee'):
            return JsonResponse(WeightMeasurementSerializer(user.trainee.all_measurements, many=True).data, safe=False)

        return JsonResponse({'error': 'User is not a trainee'}, status=403)

    def post(self, request):
        try:
            data = self.request.data
            trainee = data.get('trainee')
            user = request.user
            if user.trainee.id != trainee:
                raise ValidationError("User does not match trainee")
            with transaction.atomic():
                trainee = Trainee.objects.get(id=trainee)
                measurement = WeightMeasurement.objects.create(
                    trainee=trainee,
                    user_input_date=data.get('user_input_date'),
                    value=data.get('value')
                )
            return JsonResponse({
                "message": "Measurement created in successfully",
                "measurement": WeightMeasurementSerializer(measurement).data
            }, status=201)

        except Exception as e:
            return JsonResponse({"message": f"{e!r}"}, status=500)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class WeightMeasurementDetail(APIView, WeightMeasurementPermission):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [permissions.IsAuthenticated, WeightMeasurementPermission]
    serializer_class = WeightMeasurementSerializer

    @staticmethod
    def get(request, pk):
        try:
            measurement = WeightMeasurement.objects.get(id=pk)
            if request.user.trainee.id != measurement.trainee.id:
                return JsonResponse({"message": "User does not match trainee"}, status=403)
            return JsonResponse(WeightMeasurementSerializer(measurement).data, safe=False)
        except Exception as e:
            return JsonResponse({"message": f"{e!r}"}, status=500)

    @staticmethod
    def delete(request, pk):
        try:
            measurement = WeightMeasurement.objects.get(id=pk)
            if request.user.trainee.id != measurement.trainee.id:
                return JsonResponse({"message": "User does not match trainee"}, status=403)
            measurement.delete()
            return JsonResponse({"message": "Measurement deleted successfully", "measurement": {"id": pk}}, status=203)
        except WeightMeasurement.DoesNotExist:
            return JsonResponse({"message": "Measurement does not exist"}, status=404)
        except Exception as e:
            return JsonResponse({"message": f"{e!r}"}, status=500)

    @staticmethod
    def put(request, pk):
        try:
            measurement = WeightMeasurement.objects.get(id=pk)
            if request.user.trainee.id != measurement.trainee.id:
                return JsonResponse({"message": "User does not match trainee"}, status=403)
            data = request.data
            measurement.user_input_date = data.get('user_input_date')
            measurement.value = data.get('value')
            measurement.save()
            return JsonResponse({
                "message": "Measurement updated successfully",
                "measurement": WeightMeasurementSerializer(measurement).data
            }, safe=False)
        except Exception as e:
            return JsonResponse({"message": f"{e!r}"}, status=500)
