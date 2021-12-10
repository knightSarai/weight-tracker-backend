from django.db import models
from django.contrib.auth.models import User


class Trainer(models.Model):
    user = models.OneToOneField(
        User, related_name='trainer', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.username
