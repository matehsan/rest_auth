from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework import status

from auth.views import UserProfile


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class UserTests(TestCase):
    """user test"""

    def setUp(self):
        self.client = APIClient()

        self.user_data = {
            "username": 'user',
            "email": 'user@user.com',
            "password": 'user123456'
        }
        create_user(**self.user_data)

    def test_create_user(self):
        """create user tests"""
        payload = {
            "username": 'test',
            "email": 'test@test.com',
            "password": '123456'
        }
        res = self.client.post('/api/create/', payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data['data'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data['data'])

    def test_create_user_exists(self):
        res = self.client.post('/api/create/', self.user_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_login_ok(self):
        """token auth test"""
        payload = {
            "username": self.user_data['username'],
            "password": self.user_data['password']
        }
        user = get_user_model().objects.get(username=self.user_data['username'])
        res = self.client.post('/api/login/', payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # check token
        self.assertEqual(res.data['token'], Token.objects.get(user=user).key)

    def test_token_login_not_ok(self):
        wrong_user_payload = {
            "username": 'user',
            "password": 'wrong'
        }
        res = self.client.post('/api/login/', wrong_user_payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_login_no_user(self):
        payload = {
            "username": 'nouser',
            "password": '123456'
        }
        res = self.client.post('/api/login/', payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_info(self):
        user = get_user_model().objects.get(username=self.user_data['username'])

        user_info_request_factory = APIRequestFactory()
        user_profile_view = UserProfile.as_view()

        request = user_info_request_factory.get('/api/user/')

        force_authenticate(request, user=user)

        res = user_profile_view(request)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['username'], self.user_data['username'])
        # TODO hameye halat

    def test_get_user_info_token_base(self):
        payload = {
            "username": self.user_data['username'],
            "password": self.user_data['password']
        }

        res = self.client.post('/api/login/', payload)
        token = res.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        res2 = self.client.get('/api/user/')

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data[0]['username'], payload['username'])

    def test_get_user_info_unauthorized(self):
        res = self.client.get('/api/user/')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_password(self):
        payload = {
            "username": self.user_data['username'],
            "password": self.user_data['password']
        }

        res = self.client.post('/api/login/', payload)
        token = res.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        passwords = {
            'old_password': self.user_data['password'],
            'new_password': 'salam123'
        }

        res2 = self.client.put('/api/user/password/', passwords)

        self.assertEqual(res2.status_code, status.HTTP_200_OK)

    def test_change_password_wrong_password(self):
        payload = {
            "username": self.user_data['username'],
            "password": self.user_data['password']
        }

        res = self.client.post('/api/login/', payload)
        token = res.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        passwords = {
            'old_password': 'wrong_password',
            'new_password': 'no_matter'
        }

        res2 = self.client.put('/api/user/password/', passwords)

        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_unauthorized(self):
        res = self.client.put('/api/user/password/')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
