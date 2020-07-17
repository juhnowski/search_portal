from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

User = get_user_model()

client = APIClient()


class UserTestCase(APITestCase):
    fixtures = ['fixtures/users.json', 'fixtures/documents.json']

    def setUp(self):
        self.user = User.objects.get(email='admin@gmail.com')
        self.token = Token.objects.create(user=self.user)

    def test_create_record(self):
        response = client.post('/api/v1/statistics/create/', HTTP_AUTHORIZATION='Token' + ' ' + self.token.key)
        self.assertEqual(response.status_code, 201)

    def test_get_total_analytics_1(self):
        response = client.get('/api/v1/statistics/', HTTP_AUTHORIZATION='Token' + ' ' + self.token.key)
        self.assertEqual(response.status_code, 200)

    def test_get_total_analytics_2(self):
        response = client.get('/api/v1/statistics/last/', HTTP_AUTHORIZATION='Token' + ' ' + self.token.key)
        self.assertEqual(response.status_code, 200)

    def test_get_total_documents(self):
        response = client.get('/api/v1/statistics/documents/', HTTP_AUTHORIZATION='Token' + ' ' + self.token.key)
        self.assertEqual(response.status_code, 200)

    def test_get_total_users(self):
        response = client.get('/api/v1/statistics/users/', HTTP_AUTHORIZATION='Token' + ' ' + self.token.key)
        self.assertEqual(response.status_code, 200)

    def test_get_total_companies(self):
        response = client.get('/api/v1/statistics/companies/', HTTP_AUTHORIZATION='Token' + ' ' + self.token.key)
        self.assertEqual(response.status_code, 200)

    def test_get_total_notes(self):
        response = client.get('/api/v1/statistics/notes/', HTTP_AUTHORIZATION='Token' + ' ' + self.token.key)
        self.assertEqual(response.status_code, 200)
