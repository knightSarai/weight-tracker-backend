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
