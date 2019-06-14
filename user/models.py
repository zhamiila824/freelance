from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE = (
        ('customer', 'Customer'),
        ('executor', 'Executor'),
    )
    role = models.CharField(choices=ROLE, max_length=8)
    balance = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username
