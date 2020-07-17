from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from users.models import Company

User = get_user_model()

client = APIClient()

class UserTestCase(APITestCase):

    def setUp(self):
        # простой юзер
        self.email = 'test@gmail.com'
        self.password = 'test123'
        self.role = 'UR'
        self.user = User.objects.create(
            email=self.email,
            password=self.password,
            role=self.role
        )
        self.user_token = Token.objects.create(user=self.user)

        # простой юзер 2
        self.email_2 = 'test_2@gmail.com'
        self.password_2 = 'test123'
        self.role = 'UR'
        self.user_2 = User.objects.create(
            email=self.email_2,
            password=self.password_2,
            role=self.role
        )
        self.user_token_2 = Token.objects.create(user=self.user_2)

        # superuser
        self.email = 'test2@gmail.com'
        self.password = 'test123'
        self.superuser = User.objects.create_superuser(
            email=self.email,
            password=self.password,
        )
        self.superuser_token = Token.objects.create(user=self.superuser)

        # компания
        self.company = Company.objects.create(company_name='Название компании',
                                              position_сompany='Должность')

    def test_get_list_users(self):
        # получить список пользователей
        response = client.get('/api/v1/users', HTTP_AUTHORIZATION='Token' + ' ' + self.superuser_token.key)
        self.assertEqual(response.status_code, 200)

    def test_get_user(self):
        # получить отдельного пользователя
        user = User.objects.get(email='test@gmail.com')
        response = client.get('/api/v1/users/' + str(self.user.id), HTTP_AUTHORIZATION='Token' + ' ' + self.user_token.key)
        self.assertEqual(response.status_code, 200)

    def test_get_user_not_permission(self):
        # получить пользователя 1 от пользователя 2
        user = User.objects.get(email='test@gmail.com')
        response = client.get('/api/v1/users/' + str(self.user.id), HTTP_AUTHORIZATION='Token' + ' ' + self.user_token_2.key)
        self.assertEqual(response.status_code, 403)

    def test_put_user(self):
        # изменить пользователя
        user = User.objects.get(email='test@gmail.com')
        data = {
            'email': 'test@example.com',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'patronymic': 'Иванович',
            'phone': '12345',
            'password': 'testUser321',
            'role': 'UR',
            'company': {
                'company_name': 'Название компании',
                'position_сompany': 'Должность'
            },

        }
        response = client.put('/api/v1/users/' + str(self.user.id), data, HTTP_AUTHORIZATION='Token' + ' ' + self.user_token.key, format='json')
        self.assertEqual(response.status_code, 200)

    def test_put_user_not_permission(self):
        # изменить пользователя
        user = User.objects.get(email='test@gmail.com')
        data = {
            'email': 'test@example.com',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'patronymic': 'Иванович',
            'phone': '12345',
            'password': 'testUser321',
            'role': 'UR',
            'company': {
                'company_name': 'Название компании',
                'position_сompany': 'Должность'
            },
        }
        response = client.put('/api/v1/users/' + str(self.user.id), data, HTTP_AUTHORIZATION='Token' + ' ' + self.user_token_2.key, format='json')
        self.assertEqual(response.status_code, 403)

    def test_post_users(self):
        # создать пользователя от админа
        data = {
            'email': 'test@example.com',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'patronymic': 'Иванович',
            'phone': '12345',
            'password': 'testUser321',
            'role': 'UR',
            'company': {
                'company_name': 'Название компании',
                'position_сompany': 'Должность'
            },
        }
        response = client.post('/api/v1/users/create', data, HTTP_AUTHORIZATION='Token' + ' ' + self.superuser_token.key, format='json')
        self.assertEqual(response.status_code, 201)

    def test_post_users(self):
        # создать пользователя не от админа
        data = {
            'email': 'test@example.com',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'patronymic': 'Иванович',
            'phone': '12345',
            'password': 'testUser321',
            'role': 'UR',
            'company': {
                'company_name': 'Название компании',
                'position_сompany': 'Должность'
            },
        }
        response = client.post('/api/v1/users/create', data, HTTP_AUTHORIZATION='Token' + ' ' + self.user_token.key, format='json')
        self.assertEqual(response.status_code, 403)


    def test_search_user(self):
        response = client.get('/api/v1/users/search/?search=test_2@gmail.com',
                              HTTP_AUTHORIZATION='Token' + ' ' + self.user_token.key)
        self.assertEqual(response.status_code, 200)
