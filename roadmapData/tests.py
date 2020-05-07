import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class PermissionTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_permission(self):
        self.client.post("/api/users/",
                         {"email": "zxz@qq.com", "password": "minjie", "username": "zxz"},
                         format='json')
        response = self.client.post("/api/login/",
                                    {"username": "zxz", "password": "minjie"},
                                    format='json')
        token = json.loads(response.content)["token"]

        response = self.client.post("/api/articles/",
                                    {"title": "my book", "author": "zxz", "journal": "science", "volume": 1, "pages": 2,
                                     "years": 1998, "url": "http://www.baidu.com"},
                                    HTTP_AUTHORIZATION="JWT " + token, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AuthTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth(self):
        response = self.client.post("/api/users/",
                                    {"email": "zxz@qq.com", "password": "minjie", "username": "zxz"},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post("/api/login/",
                                    {"username": "zxz", "password": "minjie"},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = json.loads(response.content)["token"]
        response = self.client.post("/api/verify/",
                                    {"token": token},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post("/api/refresh/",
                                    {"token": token},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
