from django.db import models
from django.contrib.auth.models import User


class Trainee(models.Model):
    user = models.OneToOneField(
        User, related_name='trainee', on_delete=models.CASCADE
    )
    trainer = models.ForeignKey(
        'trainers.Trainer', related_name='all_trainees', on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.user.username

    @property
    def name(self):
        return self.user.username


class WeightMeasurement(models.Model):
    trainee = models.ForeignKey(
        'trainees.Trainee',
        related_name='all_trainee_measurements',
        on_delete=models.DO_NOTHING,
    )
    UOM = models.CharField('Unit Of Measurement', max_length=10, default='kg')
    created_at = models.DateTimeField('Created at', auto_now_add=True, editable=False)
    updated_at = models.DateTimeField('Updated at', auto_now=True)
    value = models.CharField('value', max_length=255, null=False)

    def __str__(self):
        return f'{self.trainee.name}: {self.value}{self.UOM}'
