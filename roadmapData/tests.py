import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase


# Create your tests here.
class BasicTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_user_post(self):
        # check post
        data = {
            "email": "zhuziyu.edward@gmail.com",
            "password": "minjie",
            "username": "zzy"
        }
        response = self.client.post("/api/users/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # check get
        response = self.client.get("/api/users/1.json", format='json')
        self.assertEqual(response.status_code, 200)

        # check content
        response_content = json.loads(response.content)
        self.assertEqual(response_content["username"], "zzy")
        self.assertEqual(response_content["password"], "minjie")
        self.assertEqual(response_content["email"], "zhuziyu.edward@gmail.com")

    def test_article_post(self):
        # check post
        data = {
            "title": "my book",
            "author": "zzy",
            "journal": "science",
            "volume": 1,
            "pages": 2,
            "years": 1998,
            "url": "http://www.baidu.com"
        }
        response = self.client.post("/api/articles/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check get
        response = self.client.get("/api/articles/1.json", format='json')
        self.assertEqual(response.status_code, 200)

        # check content
        response_content = json.loads(response.content)
        self.assertEqual(response_content["title"], "my book")
        self.assertEqual(response_content["author"], "zzy")
        self.assertEqual(response_content["journal"], "science")
        self.assertEqual(response_content["volume"], 1)
        self.assertEqual(response_content["pages"], 2)
        self.assertEqual(response_content["years"], 1998)
        self.assertEqual(response_content["url"], "http://www.baidu.com")