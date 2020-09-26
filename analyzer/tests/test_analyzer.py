from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from analyzer.models import Profile


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


def create_profile(**kwargs):
    return Profile.objects.create(**kwargs)


class AnalyzerTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        self.user_data = {
            "username": 'user',
            "email": 'user@user.com',
            "password": 'user123456'
        }
        user = create_user(**self.user_data)

        self.profile_data = {
            "user": user,
            "role": 3,
            "phone": 9122222222,
            "email": "user@user.com",
            "bot_user_id": "123456789",
            "bot_first_name": "",
            "bot_last_name": "",
            "bot_username": "",
            "bot_expected_value": "",
            "bot_future_expected_value": ""
        }

        create_profile(**self.profile_data)

    def test_create_analyzer_profile(self):
        payload = {
            "user": {
                "username": "test",
                "email": "test@test.com",
                "password": "salam123456"
            },
            "role": 3,
            "phone": 9122222222,
            "email": "test@test.com",
            "bot_user_id": "123456",
            "bot_first_name": "",
            "bot_last_name": "",
            "bot_username": "",
            "bot_expected_value": "",
            "bot_future_expected_value": ""
        }

        res = self.client.post('/analysts', payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['user']['username'], payload['user']['username'])

    def test_create_an_exist_analyzer(self):
        res = self.client.post('/analysts', self.profile_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_list(self):
        res = self.client.get('/analysts')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user_data['username'], res.data[0]['user']['username'])

    def test_create_and_get(self):
        payload = {
            "user": {
                "username": "test",
                "email": "test@test.com",
                "password": "salam123456"
            },
            "role": 3,
            "phone": 9122222222,
            "email": "test@test.com",
            "bot_user_id": "123456",
            "bot_first_name": "",
            "bot_last_name": "",
            "bot_username": "",
            "bot_expected_value": "",
            "bot_future_expected_value": ""
        }

        res = self.client.post('/analysts', payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['user']['username'], payload['user']['username'])

        res2 = self.client.get('/analysts')

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(payload['user']['username'], res2.data[-1]['user']['username'])
