import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase


# Create your tests here.
class ModelTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        data = {
            "password": "minjie",
            "username": "zzy"
        }
        response = self.client.post("/api/users/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_model(self):
        # get token
        data = {
            "password": "minjie",
            "username": "zzy"
        }
        response = self.client.post("/api/login/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_token = json.loads(response.content)['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + user_token)

    def test_article_model(self):
        # get token
        data = {
            "password": "minjie",
            "username": "zzy"
        }
        response = self.client.post("/api/login/", data, format='json')
        user_token = json.loads(response.content)['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + user_token)

        # post
        data = {
            "title": "my article",
            "author": "edward"
        }
        response = self.client.post("/api/articles/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = json.loads(response.content)

        # get
        response = self.client.get("/api/articles/1.json", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = json.loads(response.content)
        self.assertEqual(response_content["title"], "my article")
        self.assertEqual(response_content["author"], "edward")

        # update
        data = {
            "pages": "8",
        }
        response = self.client.put("/api/articles/1.json", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = json.loads(response.content)
        self.assertEqual(response_content["pages"], 8)

        # delete
        response = self.client.delete("/api/articles/1.json", format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get("/api/articles/1.json", format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_essay_model(self):
        # get token
        data = {
            "password": "minjie",
            "username": "zzy"
        }
        response = self.client.post("/api/login/", data, format='json')
        user_token = json.loads(response.content)['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + user_token)

        # post
        data = {
            "title": "my essay",
            "text": "first essay"
        }
        response = self.client.post("/api/essays/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # get
        response = self.client.get("/api/essays/1.json", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = json.loads(response.content)
        self.assertEqual(response_content["title"], "my essay")
        self.assertEqual(response_content["text"], "first essay")

        # update
        data = {
            "text": "12345",
        }
        response = self.client.put("/api/essays/1.json", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = json.loads(response.content)
        self.assertEqual(response_content["text"], "12345")

        # delete
        response = self.client.delete("/api/essays/1.json", format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get("/api/essays/1.json", format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_road_map_model(self):
        # get token
        data = {
            "password": "minjie",
            "username": "zzy"
        }
        response = self.client.post("/api/login/", data, format='json')
        user_token = json.loads(response.content)['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + user_token)

        # post
        data = {
            "title": "my roadmap",
            "text": "pwd ss"
        }
        response = self.client.post("/api/road_maps/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = json.loads(response.content)

        # get
        response = self.client.get("/api/road_maps/", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = json.loads(response.content)
        self.assertEqual(response_content[0]['title'], "my roadmap")

        response = self.client.get("/api/road_maps/1.json", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = json.loads(response.content)
        self.assertEqual(response_content["title"], "my roadmap")
        self.assertEqual(response_content["text"], "pwd ss")

        # update
        data = {
            "road_maps": ["1"]
        }
        response = self.client.put("/api/road_maps/1.json", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = json.loads(response.content)
        self.assertEqual(response_content["road_maps"], [1])

        # delete
        response = self.client.delete("/api/road_maps/1.json", format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get("/api/road_maps/1.json", format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_feed_back_model(self):
        # post
        data = {
            "text": "This product is great"
        }
        response = self.client.post("/api/feedback/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = json.loads(response.content)

    def test_tag_model(self):
        # get token
        data = {
            "password": "minjie",
            "username": "zzy"
        }
        response = self.client.post("/api/login/", data, format='json')
        user_token = json.loads(response.content)['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + user_token)

        # post
        data = {
            "name": "leetcode"
        }
        response = self.client.post("/api/tags/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = json.loads(response.content)

        # get
        response = self.client.get("/api/tags/1.json", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = json.loads(response.content)
        self.assertEqual(response_content['name'], "leetcode")

        # update
        data = {
            "name": "codeforces"
        }
        response = self.client.put("/api/tags/1.json", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = json.loads(response.content)
        self.assertEqual(response_content["name"], "codeforces")

        # delete
        response = self.client.delete("/api/tags/1.json", format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get("/api/tags/1.json", format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PermissionTest(APITestCase):
    def setUp(self):
        self.setUpTestData()

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
        article_id = response.data['id']

        response = self.client1.get("/api/articles/%d.json" % article_id, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client1.get("/api/articles/%d.json" % article_id,
                                    HTTP_AUTHORIZATION=self.http_authorization1,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client1.get("/api/articles/200.json",
                                    HTTP_AUTHORIZATION=self.http_authorization1,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client2.get("/api/articles/%d.json" % article_id,
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
        essay_id = response.data['id']

        response = self.client1.get("/api/essays/%d.json" % essay_id, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client1.get("/api/essays/%d.json" % essay_id,
                                    HTTP_AUTHORIZATION=self.http_authorization1,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client1.get("/api/essays/200.json",
                                    HTTP_AUTHORIZATION=self.http_authorization1,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client2.get("/api/essays/%d.json" % essay_id,
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
        rm_id = response.data['id']

        response = self.client1.get("/api/road_maps/%d.json" % rm_id, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client1.get("/api/road_maps/%d.json" % rm_id,
                                    HTTP_AUTHORIZATION=self.http_authorization1,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client1.get("/api/road_maps/200.json",
                                    HTTP_AUTHORIZATION=self.http_authorization1,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client2.get("/api/road_maps/%d.json" % rm_id,
                                    HTTP_AUTHORIZATION=self.http_authorization2,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client1.post("/api/share/roadmap/", {"id": rm_id},
                                     HTTP_AUTHORIZATION=self.http_authorization1,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_roadmap_share_permission(self):
        response = self.client1.post("/api/road_maps/",
                                     {"title": "my roadmap", "text": "{}", "description": "description"},
                                     HTTP_AUTHORIZATION=self.http_authorization1,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        rm_id = response.data['id']

        response = self.client1.post("/api/share/roadmap/", {"id": 10},
                                     HTTP_AUTHORIZATION=self.http_authorization1,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client1.post("/api/share/roadmap/", {"id": rm_id},
                                     HTTP_AUTHORIZATION=self.http_authorization1,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        share_id = json.loads(response.content)["share_id"]
        response = self.client2.get("/api/share/roadmap/" + share_id + "/",
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client2.get("/api/share/roadmap/%d/" % rm_id,
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
