from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

User = get_user_model()

client = APIClient()


class UserTestCase(APITestCase):
    fixtures = ['fixtures/users.json', 'fixtures/documents.json']

    def setUp(self):
        self.user_admin = User.objects.get(email='admin@gmail.com')

        self.email_user = 'user@example.com'
        self.password_1 = 'test123'

        self.email_reader = 'reader@example.com'
        self.password_2 = 'test321'

        self.email_library = 'library@example.com'
        self.password_3 = 'test567'

        self.email_expert = 'expert@example.com'
        self.password_4 = 'test56d7'

        self.email_group_admin = 'groupadmin@example.com'
        self.password_5 = 'test5d67'

        self.user_user = User.objects.create_user(
            email=self.email_user,
            password=self.password_1,
            role='UR'
        )

        self.user_reader = User.objects.create_user(
            email=self.email_reader,
            password=self.password_2,
            role='RD'
        )

        self.user_library = User.objects.create_user(
            email=self.email_library,
            password=self.password_3,
            role='BL'
        )

        self.user_expert = User.objects.create_user(
            email=self.email_expert,
            password=self.password_4,
            role='EX'
        )

        self.user_group_admin = User.objects.create_user(
            email=self.email_group_admin,
            password=self.password_5,
            role='GA'
        )

        self.token_admin = Token.objects.create(user=self.user_admin)
        self.token_user = Token.objects.create(user=self.user_user)
        self.token_reader = Token.objects.create(user=self.user_reader)
        self.token_library = Token.objects.create(user=self.user_library)
        self.token_expert = Token.objects.create(user=self.user_expert)
        self.token_group_admin = Token.objects.create(user=self.user_group_admin)

    def test_get_document_rating(self):
        # получение рейтинга документа

        response_admin = client.get('/api/v1/documents/1',
                                    HTTP_AUTHORIZATION='Token' + ' ' + self.token_admin.key)

        response_user = client.get('/api/v1/documents/1',
                                   HTTP_AUTHORIZATION='Token' + ' ' + self.token_user.key)

        response_reader = client.get('/api/v1/documents/1',
                                     HTTP_AUTHORIZATION='Token' + ' ' + self.token_reader.key)

        response_library = client.get('/api/v1/documents/1',
                                      HTTP_AUTHORIZATION='Token' + ' ' + self.token_library.key)

        response_expert = client.get('/api/v1/documents/1',
                                     HTTP_AUTHORIZATION='Token' + ' ' + self.token_expert.key)

        response_group_admin = client.get('/api/v1/documents/1',
                                          HTTP_AUTHORIZATION='Token' + ' ' + self.token_group_admin.key)

        self.assertEqual(response_admin.status_code, 200)
        self.assertEqual(response_user.status_code, 200)
        self.assertEqual(response_reader.status_code, 200)
        self.assertEqual(response_library.status_code, 200)
        self.assertEqual(response_expert.status_code, 200)
        self.assertEqual(response_group_admin.status_code, 403)

    def test_rate_document(self):
        # проставление оценки на документ

        response_admin = client.post('/api/v1/documents/1/rate',
                                     {'value': 2},
                                     format='json',
                                     HTTP_AUTHORIZATION='Token' + ' ' + self.token_admin.key)
        response_user = client.post('/api/v1/documents/1/rate',
                                    {'value': 2},
                                    format='json',
                                    HTTP_AUTHORIZATION='Token' + ' ' + self.token_user.key)
        response_reader = client.post('/api/v1/documents/1/rate',
                                      {'value': 3},
                                      format='json',
                                      HTTP_AUTHORIZATION='Token' + ' ' + self.token_reader.key)
        response_library = client.post('/api/v1/documents/1/rate',
                                       {'value': 4},
                                       format='json',
                                       HTTP_AUTHORIZATION='Token' + ' ' + self.token_library.key)
        response_expert = client.post('/api/v1/documents/1/rate',
                                      {'value': 4},
                                      format='json',
                                      HTTP_AUTHORIZATION='Token' + ' ' + self.token_expert.key)
        response_group_admin = client.post('/api/v1/documents/1/rate',
                                           {'value': 4},
                                           format='json',
                                           HTTP_AUTHORIZATION='Token' + ' ' + self.token_group_admin.key)

        # root
        self.assertEqual(response_admin.status_code, 201)
        # user UR
        self.assertEqual(response_user.status_code, 201)
        # reader RD
        self.assertEqual(response_reader.status_code, 201)
        # library BL
        self.assertEqual(response_library.status_code, 201)
        # expert EX
        self.assertEqual(response_expert.status_code, 201)
        # group admin GA
        self.assertEqual(response_group_admin.status_code, 403)

        # попытка оценить документ дважды
        response_admin = client.post('/api/v1/documents/1/rate',
                                     {'value': 3},
                                     format='json',
                                     HTTP_AUTHORIZATION='Token' + ' ' + self.token_admin.key)
        response_user = client.post('/api/v1/documents/1/rate',
                                    {'value': 3},
                                    format='json',
                                    HTTP_AUTHORIZATION='Token' + ' ' + self.token_user.key)
        response_reader = client.post('/api/v1/documents/1/rate',
                                      {'value': 4},
                                      format='json',
                                      HTTP_AUTHORIZATION='Token' + ' ' + self.token_reader.key)
        response_library = client.post('/api/v1/documents/1/rate',
                                       {'value': 5},
                                       format='json',
                                       HTTP_AUTHORIZATION='Token' + ' ' + self.token_library.key)

        response_expert = client.post('/api/v1/documents/1/rate',
                                      {'value': 5},
                                      format='json',
                                      HTTP_AUTHORIZATION='Token' + ' ' + self.token_expert.key)

        response_group_admin = client.post('/api/v1/documents/1/rate',
                                           {'value': 5},
                                           format='json',
                                           HTTP_AUTHORIZATION='Token' + ' ' + self.token_group_admin.key)

        # root
        self.assertEqual(response_admin.status_code, 400)
        # user UR
        self.assertEqual(response_user.status_code, 400)
        # reader RD
        self.assertEqual(response_reader.status_code, 400)
        # library BL
        self.assertEqual(response_library.status_code, 400)
        # expert EX
        self.assertEqual(response_expert.status_code, 400)
        # group admin GA
        self.assertEqual(response_group_admin.status_code, 403)
