from django.test import TestCase

from rest_framework import status

from .models import Task
from user.models import User


class TaskTest(TestCase):
    base_url = 'http://127.0.0.1:8000/api/v1'
    sign_in_url = 'http://127.0.0.1:8000/api/vi/auth/sign_in'
    executor_data = {
        'username': 'executor',
        'password': '12345'
    }
    customer_data = {
        'username': 'customer',
        'password': '12345'
    }

    def setUp(self):
        self.customer = User.objects.create(
            username='customer',
            password='12345',
            email="customer@mail.com",
            role=0,
            balance=1000
        )
        self.customer.set_password('12345')
        self.customer.save(update_fields=['password'])

        self.executor = User.objects.create(
            username='executor',
            password='12345',
            email="executor@mail.com",
            role=1,
            balance=500
        )
        self.executor.set_password('12345')
        self.executor.save(update_fields=['password'])

        self.task = Task.objects.create(
            customer=self.customer,
            title='Web site',
            description='Online queue for hospitals',
            price=100
        )

    def test_task_list(self):
        url = '%s/tasks' % self.base_url
        view = self.client.get(url)
        self.assertEqual(view.status_code, status.HTTP_200_OK)

    def test_create_task_unauthorized(self):
        url = '%s/tasks/add' % self.base_url
        view = self.client.get(url)
        self.assertEqual(view.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task_executor(self):
        self.client.post(self.sign_in_url, self.executor_data)
        url = '%s/tasks/add' % self.base_url
        data = {
            'title': 'Web site',
            'description': 'Online queue for hospitals',
            'price': '100'
        }
        view = self.client.post(url, data)
        self.assertEqual(view.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_task_balance(self):
        self.client.post(self.sign_in_url, self.customer_data)
        url = '%s/tasks/add' % self.base_url
        data = {
            'title': 'Web site',
            'description': 'Online queue for hospitals',
            'price': '10000'
        }
        view = self.client.post(url, data)
        self.assertEqual(view.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_create_task(self):
        self.client.post(self.sign_in_url, self.customer_data)
        url = '%s/tasks/add' % self.base_url
        data = {
            'title': 'Web site',
            'description': 'Online queue for hospitals',
            'price': '100'
        }
        view = self.client.post(url, data)
        self.assertEqual(view.status_code, status.HTTP_201_CREATED)

    def test_task_detail_unauthorized(self):
        url = '%s/tasks/1' % self.base_url
        view = self.client.get(url)
        self.assertEqual(view.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_task_detail_customer(self):
        self.client.post(self.sign_in_url, self.customer_data)
        url = '%s/tasks/1' % self.base_url
        view = self.client.patch(url)
        self.assertEqual(view.status_code, status.HTTP_403_FORBIDDEN)

    def test_task_detail_executor(self):
        self.client.post(self.sign_in_url, self.executor_data)
        url = '%s/tasks/1' % self.base_url
        view = self.client.patch(url)
        self.assertEqual(view.status_code, status.HTTP_202_ACCEPTED)

    def test_task_detail_done(self):
        self.client.post(self.sign_in_url, self.executor_data)
        url = '%s/tasks/1' % self.base_url
        self.client.patch(url)
        view = self.client.patch(url)
        self.assertEqual(view.status_code, status.HTTP_423_LOCKED)
