from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

User = get_user_model()
client = APIClient()


class JournalTestCase(APITestCase):
    PATH = '/api/v1/adm/import-journal'
    fixtures = ['fixtures/users.json', 'fixtures/import_journal.json']

    def setUp(self):
        self._user = User.objects.get(email='admin@gmail.com')
        self._auth_header = 'Token ' + Token.objects.create(user=self._user).key

    def test_get_all(self):
        response = client.get(self.PATH, HTTP_AUTHORIZATION=self._auth_header)
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertNotEqual(json['count'], 0)

    def test_get_xml(self):
        """ Тестируем фильтрацию. """
        response = client.get(
            self.PATH, {'type': 'xml'}, HTTP_AUTHORIZATION=self._auth_header
        )
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertNotEqual(json['count'], 0)
        for record in json['results']:
            self.assertEqual(record['type'], 'xml')
