from django.test import TestCase
from rest_framework import status
from .models import Task
from user.models import User


class TaskTest(TestCase):

    def setUp(self):
        self.customer = User.objects.create(
            username='customer',
            password='12345',
            email="customer@mail.com",
            role="customer",
            balance=1000
        )
        self.executor = User.objects.create(
            username='executor',
            password='12345',
            email="executor@mail.com",
            role="executor",
            balance=500
        )
        self.task = Task.objects.create(
            customer=self.customer,
            title='Web site',
            description='Online queue for hospitals',
            price=100
        )

    def test_string_representation(self):
        task = Task(title="Web", price=500)
        self.assertEqual(str(task), (task.title +"    "+str(task.price)))


class ViewsTest(TestCase):
    base_url = 'http://127.0.0.1:8000/api/v1'

    def test_task_list(self):
        url = '%s/tasks' % self.base_url
        view = self.client.get(url)
        self.assertEqual(view.status_code, status.HTTP_200_OK)

    def test_task_detail_unauthorized(self):
        url = '%s/tasks/1' % self.base_url
        view = self.client.get(url)
        self.assertEqual(view.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task_unauthorized(self):
        url = '%s/tasks/add' % self.base_url
        view = self.client.get(url)
        self.assertEqual(view.status_code, status.HTTP_401_UNAUTHORIZED)
