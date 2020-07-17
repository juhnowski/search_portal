from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework.utils import json

User = get_user_model()

client = APIClient()


def docs_id(docs):
    result = []
    for d in docs:
        result.append(d.get('id'))
    return result


class UserTestCase(APITestCase):
    fixtures = ['fixtures/users.json', 'fixtures/search_document.json']

    def setUp(self):
        self.user = User.objects.get(email='admin@gmail.com')
        self.token = Token.objects.create(user=self.user)
        from infoportal.search.engines.sphinx.builder import SphinxIndexBuilder
        ib = SphinxIndexBuilder()
        ib.build()

    def test_1_1(self):
        expectation = [705, 865, 420, 423, 777, 906, 747, 1006, 272, 977]
        response = client.post(
            '/api/v1/search/text?limit=10&offset=0',
            {"search_text": "акустика", "page_size": "30", "search_options": "{}"},
            HTTP_AUTHORIZATION='Token' + ' ' + self.token.key,
            format='json'
        )
        result = docs_id(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expectation)

    def test_1_2(self):
        expectation = [659, 1012, 501, 344, 861]
        response = client.post(
            '/api/v1/search/text?limit=10&offset=10',
            {"search_text": "акустика", "page_size": "30", "search_options": "{}"},
            HTTP_AUTHORIZATION='Token' + ' ' + self.token.key,
            format='json'
        )
        result = docs_id(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expectation)

    def test_2_1(self):
        expectation = [705, 865, 420, 423, 777, 906, 747, 1006, 272, 977]
        response = client.post(
            '/api/v1/search/text?limit=10&offset=0',
            {"search_text": "акустикой", "page_size": "30", "search_options": "{}"},
            HTTP_AUTHORIZATION='Token' + ' ' + self.token.key,
            format='json'
        )
        result = docs_id(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expectation)

    def test_2_2(self):
        expectation = [659, 1012, 501, 344, 861]
        response = client.post(
            '/api/v1/search/text?limit=10&offset=10',
            {"search_text": "акустикой", "page_size": "30", "search_options": "{}"},
            HTTP_AUTHORIZATION='Token' + ' ' + self.token.key,
            format='json'
        )
        result = docs_id(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expectation)

    def test_3(self):
        expectation = []
        response = client.post(
            '/api/v1/search/text?limit=10&offset=0',
            {"search_text": "куст", "page_size": "30", "search_options": "{}"},
            HTTP_AUTHORIZATION='Token' + ' ' + self.token.key,
            format='json'
        )
        result = docs_id(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expectation)

    def test_4(self):
        expectation = []
        response = client.post(
            '/api/v1/search/text?limit=10&offset=0',
            {"search_text": "кустик", "page_size": "30", "search_options": "{}"},
            HTTP_AUTHORIZATION='Token' + ' ' + self.token.key,
            format='json'
        )
        result = docs_id(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expectation)

    def test_5(self):
        expectation = []
        response = client.post(
            '/api/v1/search/text?limit=10&offset=0',
            {"search_text": "кустиком", "page_size": "30", "search_options": "{}"},
            HTTP_AUTHORIZATION='Token' + ' ' + self.token.key,
            format='json'
        )
        result = docs_id(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expectation)

    def test_6(self):
        expectation = [559, 592, 1012, 597, 1045, 703]
        response = client.post(
            '/api/v1/search/text?limit=10&offset=0',
            {"search_text": "акустический", "page_size": "30", "search_options": "{}"},
            HTTP_AUTHORIZATION='Token' + ' ' + self.token.key,
            format='json'
        )
        result = docs_id(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expectation)

    def test_7(self):
        expectation = [559, 592, 1012, 597, 1045, 703]
        response = client.post(
            '/api/v1/search/text?limit=10&offset=0',
            {"search_text": "акустической", "page_size": "30", "search_options": "{}"},
            HTTP_AUTHORIZATION='Token' + ' ' + self.token.key,
            format='json'
        )
        result = docs_id(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expectation)

    def test_8(self):
        expectation = [488, 592, 597, 559]
        response = client.post(
            '/api/v1/search/text?limit=10&offset=0',
            {"search_text": "Экраны акустические", "page_size": "30", "search_options": "{}"},
            HTTP_AUTHORIZATION='Token' + ' ' + self.token.key,
            format='json'
        )
        result = docs_id(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expectation)

    def test_9(self):
        expectation = [488, 592, 597, 559]
        response = client.post(
            '/api/v1/search/text?limit=10&offset=0',
            {"search_text": "акустические экраны", "page_size": "30", "search_options": "{}"},
            HTTP_AUTHORIZATION='Token' + ' ' + self.token.key,
            format='json'
        )
        result = docs_id(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expectation)

    def test_10(self):
        expectation = [559]
        response = client.post(
            '/api/v1/search/text?limit=10&offset=0',
            {"search_text": "акустическим экранам", "page_size": "30", "search_options": "{}"},
            HTTP_AUTHORIZATION='Token' + ' ' + self.token.key,
            format='json'
        )
        result = docs_id(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expectation)

    def test_11(self):
        expectation = [1012]
        response = client.post(
            '/api/v1/search/text?limit=10&offset=0',
            {"search_text": "акустических характеристик", "page_size": "30", "search_options": "{}"},
            HTTP_AUTHORIZATION='Token' + ' ' + self.token.key,
            format='json'
        )
        result = docs_id(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expectation)

    def test_12(self):
        expectation = [597]
        response = client.post(
            '/api/v1/search/text?limit=10&offset=0',
            {"search_text": "33329", "page_size": "30", "search_options": "{}"},
            HTTP_AUTHORIZATION='Token' + ' ' + self.token.key,
            format='json'
        )
        result = docs_id(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expectation)

    def test_13(self):
        expectation = [1012, 488, 559, 592, 597, ]
        response = client.post(
            '/api/v1/search/text?limit=10&offset=0',
            {"search_text": "Acoustical", "page_size": "30", "search_options": "{}"},
            HTTP_AUTHORIZATION='Token' + ' ' + self.token.key,
            format='json'
        )
        result = docs_id(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expectation)

    def test_14(self):
        expectation = [705, 865, 420, 423, 777, 906, 747, 1006, 272, 977,
                       659, 1012, 501, 344, 861, 488, 559, 592, 597, 1045, 703]
        response = client.post(
            '/api/v1/search/text?limit=30&offset=0',
            {"search_text": "Acoustic", "page_size": "30", "search_options": "{}"},
            HTTP_AUTHORIZATION='Token' + ' ' + self.token.key,
            format='json'
        )
        result = docs_id(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expectation)
