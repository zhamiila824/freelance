from django.test import TestCase
from rest_framework import status
from .models import User


class UserTest(TestCase):
    base_url = 'http://127.0.0.1:8000/api/v1'

    def setUp(self):
        User.objects.create(
            username="user1",
            password="password",
            first_name="user",
            last_name="customer",
            email="user1@mail.com",
            role="customer",
            balance=1000
        )

        User.objects.create(
            username="user2",
            password="password",
            first_name="user",
            last_name="executor",
            email="user2@mail.com",
            role="executor",
            balance=1000
        )

    def test_string_representation(self):
        user = User(username="user", password="123")
        self.assertEqual(str(user), user.username)


class ViewsTest(TestCase):
    base_url = 'http://127.0.0.1:8000/api/v1'

    def test_user_list(self):
        url = '%s/users' % self.base_url
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_sign_up(self):
        url = '%s/auth/sign_up' % self.base_url
        data = {
            'username': 'test_user', 'password': '123',
            'first_name': 'mira', 'last_name': 'amanturova',
            'email': 'test@gmail.com', 'role': "customer", 'balance': 1000
        }
        view = self.client.post(url, data)
        self.assertEqual(view.status_code, status.HTTP_201_CREATED)
        self.assertTrue(view.data.get('token'))

    def test_sign_up_bad_request(self):
        url = '%s/auth/sign_up' % self.base_url
        data = {
            'username': 'test_user', 'first_name': 'mira', 'last_name': 'amanturova',
            'email': 'test@gmail.com', 'role': "customer", 'balance': 1000
        }
        view = self.client.post(url, data)
        self.assertEqual(view.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_in(self):
        self.user = User.objects.create(
            username='test_user',
            password='12345',
        )
        self.user.set_password('12345')
        self.user.save(update_fields=['password'])
        url = '%s/auth/sign_in' % self.base_url
        data = {
            'username': 'test_user',
            'password': '12345'
        }
        view = self.client.post(url, data)
        self.assertEqual(view.status_code, status.HTTP_200_OK)
        self.assertTrue(view.data.get('token'))

    def test_sign_in_bad_request(self):
        self.user = User.objects.create(
            username='test_user',
            password='12345',
        )
        self.user.set_password('12345')
        self.user.save(update_fields=['password'])
        url = '%s/auth/sign_in' % self.base_url
        data = {
            'username': 'testuser',
            'password': '12345'
        }
        view = self.client.post(url, data)
        self.assertEqual(view.status_code, status.HTTP_401_UNAUTHORIZED)
