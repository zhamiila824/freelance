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
        self.assertEqual(str(task), task.title)


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

    def test_task_detail_customer(self):
        url = '%s/auth/sign_in' % self.base_url
        self.user = User.objects.create(
            username='user',
            role='customer',
            password='12345',
        )

        self.user.set_password('12345')
        self.user.save(update_fields=['password'])
        data = {
            'username': 'user',
            'password': '12345'
        }
        self.client.post(url, data)
        self.customer = User.objects.create(
            username='customer',
            password='12345',
            email="customer@mail.com",
            role="customer",
            balance=1000
        )
        self.task = Task.objects.create(
            customer=self.customer,
            title='Web site',
            description='Online queue for hospitals',
            price=100
        )
        url = '%s/tasks/1' % self.base_url
        view = self.client.patch(url)
        self.assertEqual(view.status_code, status.HTTP_403_FORBIDDEN)

    def test_task_detail_executor(self):
        url = '%s/auth/sign_in' % self.base_url
        self.user = User.objects.create(
            username='executor',
            role='executor',
            password='12345',
        )

        self.user.set_password('12345')
        self.user.save(update_fields=['password'])
        data = {
            'username': 'executor',
            'password': '12345'
        }
        self.client.post(url, data)
        self.customer = User.objects.create(
            username='customer',
            password='12345',
            email="customer@mail.com",
            role="customer",
            balance=1000
        )
        self.task = Task.objects.create(
            customer=self.customer,
            title='Web site',
            description='Online queue for hospitals',
            price=100
        )
        url = '%s/tasks/1' % self.base_url
        view = self.client.patch(url)
        self.assertEqual(view.status_code, status.HTTP_202_ACCEPTED)

    def test_task_detail_done(self):
        url = '%s/auth/sign_in' % self.base_url
        self.user = User.objects.create(
            username='executor',
            role='executor',
            password='12345',
        )
        self.user.set_password('12345')
        self.user.save(update_fields=['password'])
        data = {
            'username': 'executor',
            'password': '12345'
        }
        self.client.post(url, data)
        self.customer = User.objects.create(
            username='customer',
            password='12345',
            email="customer@mail.com",
            role="customer",
            balance=1000
        )
        self.task = Task.objects.create(
            customer=self.customer,
            title='Web site',
            description='Online queue for hospitals',
            price=100
        )
        url = '%s/tasks/1' % self.base_url
        self.client.patch(url)
        view = self.client.patch(url)
        self.assertEqual(view.status_code, status.HTTP_423_LOCKED)

    def test_task_detail_balance(self):
        url = '%s/auth/sign_in' % self.base_url
        self.user = User.objects.create(
            username='executor',
            role='executor',
            password='12345',
        )

        self.user.set_password('12345')
        self.user.save(update_fields=['password'])
        data = {
            'username': 'executor',
            'password': '12345'
        }
        self.client.post(url, data)
        self.customer = User.objects.create(
            username='customer',
            password='12345',
            email="customer@mail.com",
            role="customer",
            balance=10000
        )
        self.task = Task.objects.create(
            customer=self.customer,
            title='Web site',
            description='Online queue for hospitals',
            price=1000
        )
        self.customer.balance = 100
        self.customer.save()
        url = '%s/tasks/1' % self.base_url
        view = self.client.patch(url)
        self.assertEqual(view.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_create_task_unauthorized(self):
        url = '%s/tasks/add' % self.base_url
        view = self.client.get(url)
        self.assertEqual(view.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task_executor(self):
        url = '%s/auth/sign_in' % self.base_url
        self.user = User.objects.create(
            username='executor',
            role='executor',
            password='12345',
        )

        self.user.set_password('12345')
        self.user.save(update_fields=['password'])
        data = {
            'username': 'executor',
            'password': '12345'
        }
        self.client.post(url, data)
        url = '%s/tasks/add' % self.base_url
        data = {
            'title': 'Web site',
            'description': 'Online queue for hospitals',
            'price': '100'
        }
        view = self.client.post(url, data)
        self.assertEqual(view.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_task_balance(self):
        url = '%s/auth/sign_in' % self.base_url
        self.user = User.objects.create(
            username='customer',
            role='customer',
            password='12345',
            balance=100
        )

        self.user.set_password('12345')
        self.user.save(update_fields=['password'])
        data = {
            'username': 'customer',
            'password': '12345'
        }
        self.client.post(url, data)
        url = '%s/tasks/add' % self.base_url
        data = {
            'title': 'Web site',
            'description': 'Online queue for hospitals',
            'price': '1000'
        }
        view = self.client.post(url, data)
        self.assertEqual(view.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_create_task(self):
        url = '%s/auth/sign_in' % self.base_url
        self.user = User.objects.create(
            username='customer',
            role='customer',
            password='12345',
            balance=1000
        )

        self.user.set_password('12345')
        self.user.save(update_fields=['password'])
        data = {
            'username': 'customer',
            'password': '12345'
        }
        self.client.post(url, data)
        url = '%s/tasks/add' % self.base_url
        data = {
            'title': 'Web site',
            'description': 'Online queue for hospitals',
            'price': '100'
        }
        view = self.client.post(url, data)
        self.assertEqual(view.status_code, status.HTTP_201_CREATED)
