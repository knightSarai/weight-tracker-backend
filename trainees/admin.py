from django.contrib import admin
from .models import Trainee


@admin.register(Trainee)
class TraineeAdmin(admin.ModelAdmin):
    pass
