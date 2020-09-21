from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

url = reversed('user:create')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class UserTests(TestCase):
    """user test"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_user(self):
        """create user tests"""
        payload = {
            "username": 'test',
            "email": 'test@test.com',
            "password": '123456'
        }
        res = self.client.post('/api/create/', payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # print(res.data['data'])
        user = get_user_model().objects.get(**res.data['data'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data['data'])

    def test_user_exists(self):
        payload = {
            "username": 'test',
            "email": 'test@test.com',
            "password": '123456'
        }

        create_user(**payload)

        res = self.client.post('/api/create/', payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)



