from django.contrib import admin
from .models import Trainee, WeightMeasurement


@admin.register(Trainee)
class TraineeAdmin(admin.ModelAdmin):
    pass

@admin.register(WeightMeasurement)
class WeightMeasurementAdmin(admin.ModelAdmin):
    pass

