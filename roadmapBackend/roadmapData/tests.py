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
