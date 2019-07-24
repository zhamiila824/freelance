from django.db import models
from django.db import transaction
from django.db.models import F
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CUSTOMER = 0
    EXECUTOR = 1
    ROLE = (
        (CUSTOMER, 'Customer'),
        (EXECUTOR, 'Executor'),
    )
    role = models.SmallIntegerField(choices=ROLE, default=1)
    balance = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    promised_balance = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    email = models.EmailField(unique=True, null=False)

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
            executor.balance = F('balance') + price
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
            customer.balance = F('balance') - price
            customer.promised_balance = F('promised_balance') - price
            customer.save()
        return customer
