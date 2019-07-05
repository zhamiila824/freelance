from django.db import models
from user.models import User


class Task(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)
    executor = models.ForeignKey(User, related_name='Executor', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title
