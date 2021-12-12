from rest_framework import serializers

from .models import WeightMeasurement


class WeightMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightMeasurement
        fields = ["id", "trainee", "UOM", "updated_at", "value", "user_input_date"]
