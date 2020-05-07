import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class PermissionTest(APITestCase):
    def setUp(self):
        self.client1 = APIClient()
        self.client1.post("/api/users/",
                          {"email": "zxz@qq.com", "password": "minjie", "username": "zxz"},
                          format='json')
        response = self.client1.post("/api/login/",
                                     {"username": "zxz", "password": "minjie"},
                                     format='json')
        token1 = json.loads(response.content)["token"]
        self.http_authorization1 = "JWT " + token1

        self.client2 = APIClient()
        self.client2.post("/api/users/",
                          {"email   ": "hdl@qq.com", "password": "jiemin", "username": "hdl"},
                          format='json')
        response = self.client2.post("/api/login/",
                                     {"username": "hdl", "password": "jiemin"},
                                     format='json')
        token2 = json.loads(response.content)["token"]
        self.http_authorization2 = "JWT " + token2

    def test_article_permission(self):
        response = self.client1.post("/api/articles/",
                                     {"title": "my article", "author": "zxz", "journal": "science", "volume": 1,
                                      "pages": 2, "years": 1998, "url": "http://www.baidu.com"},
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client1.post("/api/articles/",
                                     {"title": "my article", "author": "zxz", "journal": "science", "volume": 1,
                                      "pages": 2, "years": 1998, "url": "http://www.baidu.com"},
                                     HTTP_AUTHORIZATION=self.http_authorization1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client1.get("/api/articles/1.json", format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client1.get("/api/articles/1.json",
                                    HTTP_AUTHORIZATION=self.http_authorization1,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client1.get("/api/articles/2.json",
                                    HTTP_AUTHORIZATION=self.http_authorization1,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client2.get("/api/articles/1.json",
                                    HTTP_AUTHORIZATION=self.http_authorization2,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_essay_permission(self):
        response = self.client1.post("/api/essays/",
                                     {"title": "my essay", "text": "test"},
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client1.post("/api/essays/",
                                     {"title": "my essay", "text": "test"},
                                     HTTP_AUTHORIZATION=self.http_authorization1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client1.get("/api/essays/1.json", format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client1.get("/api/essays/1.json",
                                    HTTP_AUTHORIZATION=self.http_authorization1,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client1.get("/api/essays/2.json",
                                    HTTP_AUTHORIZATION=self.http_authorization1,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client2.get("/api/essays/1.json",
                                    HTTP_AUTHORIZATION=self.http_authorization2,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_roadmap_permission(self):
        response = self.client1.post("/api/road_maps/",
                                     {"title": "my roadmap", "text": "test", "description": "description"},
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client1.post("/api/road_maps/",
                                     {"title": "my roadmap", "text": "test", "description": "description"},
                                     HTTP_AUTHORIZATION=self.http_authorization1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client1.get("/api/road_maps/1.json", format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client1.get("/api/road_maps/1.json",
                                    HTTP_AUTHORIZATION=self.http_authorization1,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client1.get("/api/road_maps/2.json",
                                    HTTP_AUTHORIZATION=self.http_authorization1,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client2.get("/api/road_maps/1.json",
                                    HTTP_AUTHORIZATION=self.http_authorization2,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client1.post("/api/share/roadmap/", {"id": 1},
                                     HTTP_AUTHORIZATION=self.http_authorization1,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_roadmap_share_permission(self):
        response = self.client1.post("/api/road_maps/",
                                     {"title": "my roadmap", "text": "{}", "description": "description"},
                                     HTTP_AUTHORIZATION=self.http_authorization1,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client1.post("/api/share/roadmap/", {"id": 10},
                                     HTTP_AUTHORIZATION=self.http_authorization1,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client1.post("/api/share/roadmap/", {"id": 1},
                                     HTTP_AUTHORIZATION=self.http_authorization1,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        share_id = json.loads(response.content)["share_id"]
        response = self.client2.get("/api/share/roadmap/" + share_id + "/",
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client2.get("/api/share/roadmap/1/",
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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
