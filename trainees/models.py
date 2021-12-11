from django.db import models
from django.contrib.auth.models import User


class Trainee(models.Model):
    user = models.OneToOneField(
        User, related_name='trainee', on_delete=models.CASCADE
    )
    trainer = models.ForeignKey(
        'trainers.Trainer',
        related_name='all_trainees',
        on_delete=models.DO_NOTHING,
        default=1
    )

    def __str__(self):
        return self.user.username

    @property
    def name(self):
        return self.user.username

    @property
    def all_measurements(self):
        return self.all_trainee_measurements.all()


class WeightMeasurement(models.Model):
    trainee = models.ForeignKey(
        'trainees.Trainee',
        related_name='all_trainee_measurements',
        on_delete=models.DO_NOTHING,
    )
    UOM = models.CharField('Unit Of Measurement', max_length=10, default='kg')
    created_at = models.DateTimeField('Created at', auto_now_add=True, editable=False)
    updated_at = models.DateTimeField('Updated at', auto_now=True)
    user_input_date = models.DateTimeField('User Measurement Date', null=True)
    value = models.CharField('value', max_length=255, null=False)

    def __str__(self):
        return f'{self.trainee.name}: {self.value}{self.UOM}'
