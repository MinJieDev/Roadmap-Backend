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

    '''
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
        '''