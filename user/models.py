from django.db import models
from django.db import transaction
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

    @classmethod
    def get_paid(cls, id, price):
        with transaction.atomic():
            executor = (
                cls.objects
                .select_for_update()
                .get(id=id)
            )
            executor.balance += price
            executor.save()
        return executor

    @classmethod
    def pay(cls, id, price):
        with transaction.atomic():
            customer = (
                cls.objects
                .select_for_update()
                .get(id=id)
            )
            customer.balance -= price
            customer.save()
        return customer
