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

        #post
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
        
        #post
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
        
        #post
        data = {
            "title": "my roadmap", 
            "text": "pwd ss"
        }
        response = self.client.post("/api/road_maps/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = json.loads(response.content)

        # get
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
