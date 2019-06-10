from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    CUSTOMER = 1
    EXECUTOR = 2
    ROLE = (
        (CUSTOMER, 'CUSTOMER'),
        (EXECUTOR, 'EXECUTOR'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE, default=CUSTOMER)
    balance = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username
