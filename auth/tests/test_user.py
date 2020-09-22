from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework import status

from auth.views import UserProfile


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class UserTests(TestCase):
    """user test"""

    def setUp(self):
        # TODO create user
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

    def test_token_login_ok(self):
        """token auth test"""
        payload = {
            "username": 'test',
            "password": '123456'
        }
        create_user(**payload)
        res = self.client.post('/api/login/', payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # TODO token dorost bashe

    def test_token_login_not_ok(self):
        payload = {
            "username": 'test',
            "password": '123456'
        }
        create_user(**payload)
        wrong_password_payload = {
            "username": 'test',
            "password": 'wrong'
        }
        res = self.client.post('/api/login/', wrong_password_payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_login_no_user(self):
        payload = {
            "username": 'test',
            "password": '123456'
        }
        res = self.client.post('/api/login/', payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_info(self):
        payload = {
            "username": 'test',
            "email": 'test@test.com',
            "password": '123456'
        }
        create_user(**payload)
        user = get_user_model().objects.get(username=payload['username'])

        user_info_request_factory = APIRequestFactory()
        user_profile_view = UserProfile.as_view()

        request = user_info_request_factory.get('/api/user/')
        # print(request.user)
        force_authenticate(request, user=user)
        # print(request)
        res = user_profile_view(request)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['username'], payload['username'])
        # TODO hameye halat

    def test_token_base_user_info(self):
        payload = {
            "username": 'test',
            "email": 'test@test.com',
            "password": '123456'
        }
        create_user(**payload)

        res = self.client.post('/api/login/', payload)
        token = res.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        res2 = self.client.get('/api/user/')

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data[0]['username'], payload['username'])

    def test_change_password(self):
        payload = {
            "username": 'test',
            "email": 'test@test.com',
            "password": '123456'
        }
        create_user(**payload)

        res = self.client.post('/api/login/', payload)
        token = res.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        passwords = {
            'old_password': '123456',
            'new_password': 'salam123'
        }

        res2 = self.client.put('/api/user/password/', passwords)

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
