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

    def test_list_documents(self):
        response = client.get('/api/v1/documents/',
                              HTTP_AUTHORIZATION='Token' + ' ' + self.token.key)
        self.assertEqual(response.status_code, 200)

    def test_get_bibliography(self):
        response = client.get('/api/v1/documents/1/bibliography',
                              HTTP_AUTHORIZATION='Token' + ' ' + self.token.key)
        self.assertEqual(response.status_code, 200)

    def test_get_document(self):
        response = client.get('/api/v1/documents/1',
                              HTTP_AUTHORIZATION='Token' + ' ' + self.token.key)
        self.assertEqual(response.status_code, 200)

    def test_get_document_pdf_content(self):
        response = client.get('/api/v1/documents/1/content',
                              HTTP_AUTHORIZATION='Token' + ' ' + self.token.key,
                              HTTP_ACCEPT='application/pdf')
        self.assertEqual(response.status_code, 200)

    def test_get_document_image_content(self):
        response = client.get('/api/v1/documents/1/content',
                              HTTP_AUTHORIZATION='Token' + ' ' + self.token.key,
                              HTTP_ACCEPT='image/jpg')
        self.assertEqual(response.status_code, 200)

    def test_get_document_html_content(self):
        response = client.get('/api/v1/documents/1/content',
                              HTTP_AUTHORIZATION='Token' + ' ' + self.token.key,
                              HTTP_ACCEPT='text/html')
        self.assertEqual(response.status_code, 200)
