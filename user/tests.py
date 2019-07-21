from django.test import TestCase

from rest_framework import status

from .models import User


class UserTest(TestCase):
    base_url = 'http://127.0.0.1:8000/api/v1'

    def setUp(self):
        self.customer = User.objects.create(
            username="user1",
            password="password",
            first_name="user",
            last_name="customer",
            email="user1@gmail.com",
            role=0,
            balance=1000
        )
        self.customer.set_password('password')
        self.customer.save(update_fields=['password'])

        self.executor = User.objects.create(
            username="user2",
            password="password",
            first_name="user",
            last_name="executor",
            email="user2@gmail.com",
            role=1,
            balance=1000
        )
        self.executor.set_password('password')
        self.executor.save(update_fields=['password'])

    def test_string_representation(self):
        user = User(username="user", password="123")
        self.assertEqual(str(user), user.username)

    def test_user_list(self):
        url = '%s/users' % self.base_url
        view = self.client.get(url)
        self.assertEqual(view.status_code, status.HTTP_200_OK)

    def test_user_detail(self):
        url = '%s/users/1' % self.base_url
        view = self.client.get(url)
        self.assertEqual(view.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sign_up(self):
        url = '%s/auth/sign_up' % self.base_url
        data = {
            'username': 'test_user', 'password': '123',
            'first_name': 'mira', 'last_name': 'amanturova',
            'email': 'test@gmail.com', 'role': 0, 'balance': 1000
        }
        view = self.client.post(url, data)
        self.assertEqual(view.status_code, status.HTTP_201_CREATED)
        self.assertTrue(view.data.get('token'))

    def test_sign_up_bad_request(self):
        url = '%s/auth/sign_up' % self.base_url
        data = {
            'username': 'test_user', 'first_name': 'mira', 'last_name': 'amanturova',
            'email': 'test@gmail.com', 'role': 0, 'balance': 1000
        }
        view = self.client.post(url, data)
        self.assertEqual(view.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_in(self):
        url = '%s/auth/sign_in' % self.base_url
        data = {
            'username': 'user1',
            'password': 'password'
        }
        view = self.client.post(url, data)
        self.assertEqual(view.status_code, status.HTTP_200_OK)
        self.assertTrue(view.data.get('token'))

    def test_sign_in_unauthorized(self):
        url = '%s/auth/sign_in' % self.base_url
        data = {
            'username': 'user',
            'password': 'password'
        }
        view = self.client.post(url, data)
        self.assertEqual(view.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sign_in_bad_request(self):
        url = '%s/auth/sign_in' % self.base_url
        data = {
            'username': 'testuser'
        }
        view = self.client.post(url, data)
        self.assertEqual(view.status_code, status.HTTP_400_BAD_REQUEST)