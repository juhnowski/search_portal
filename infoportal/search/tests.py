from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

User = get_user_model()

client = APIClient()


class SearchTestCase(APITestCase):
    fixtures = ['fixtures/users.json', 'fixtures/documents.json']


    def setUp(self):
        self.user = User.objects.get(email='admin@gmail.com')
        self.token = Token.objects.create(user=self.user)

    def test_auto_completions(self):
        response = client.post(
            '/api/v1/search/auto_completions',
            {'search_text': 'Вид', 'page_size': '10'},
            HTTP_AUTHORIZATION='Token' + ' ' + self.token.key
        )
        self.assertEqual(response.status_code, 200)

    def test_text(self):
        response = client.post(
            '/api/v1/search/text',
            {'search_text': 'ВНИИПО', 'page_size': '10'},
            HTTP_AUTHORIZATION='Token' + ' ' + self.token.key,
            format='json'
        )
        self.assertEqual(response.status_code, 200)
