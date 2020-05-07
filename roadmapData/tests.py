import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class PermissionTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.post("/api/users/",
                         {"email": "zxz@qq.com", "password": "minjie", "username": "zxz"},
                         format='json')
        response = self.client.post("/api/login/",
                                    {"username": "zxz", "password": "minjie"},
                                    format='json')
        token = json.loads(response.content)["token"]
        self.http_authorization = "JWT " + token

    def test_article_permission(self):
        response = self.client.post("/api/articles/",
                                    {"title": "my article", "author": "zxz", "journal": "science", "volume": 1,
                                     "pages": 2, "years": 1998, "url": "http://www.baidu.com"},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post("/api/articles/",
                                    {"title": "my article", "author": "zxz", "journal": "science", "volume": 1,
                                     "pages": 2, "years": 1998, "url": "http://www.baidu.com"},
                                    HTTP_AUTHORIZATION=self.http_authorization, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get("/api/articles/1.json", format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get("/api/articles/1.json",
                                   HTTP_AUTHORIZATION=self.http_authorization,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_essay_permission(self):
        response = self.client.post("/api/essays/",
                                    {"title": "my essay", "text": "test"},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post("/api/essays/",
                                    {"title": "my essay", "text": "test"},
                                    HTTP_AUTHORIZATION=self.http_authorization, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get("/api/essays/1.json", format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get("/api/essays/1.json",
                                   HTTP_AUTHORIZATION=self.http_authorization,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_roadmap_permission(self):
        response = self.client.post("/api/road_maps/",
                                    {"title": "my roadmap", "text": "test", "description": "description"},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post("/api/road_maps/",
                                    {"title": "my roadmap", "text": "test", "description": "description"},
                                    HTTP_AUTHORIZATION=self.http_authorization, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get("/api/road_maps/1.json", format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get("/api/road_maps/1.json",
                                   HTTP_AUTHORIZATION=self.http_authorization,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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
