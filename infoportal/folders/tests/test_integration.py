import json

from django.contrib.auth import get_user_model
from django.core.management import call_command

from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from folders.models import Folders
from documents.models import Documents

User = get_user_model()

client = APIClient()

class UserTestCase(APITestCase):

    def setUp(self):
        # данные первого пользователя
        self.email_1 = 'test_1@example.com'
        self.password_1 = 'test123'
        self.role = 'UR'

        # данные второго пользователя
        self.email_2 = 'test_2@example.com'
        self.password_2 = 'test321'
        self.role = 'UR'

        # данные третьего пользователя
        self.email_3 = 'test_3@example.com'
        self.password_3 = 'test567'
        self.role = 'UR'

        # создание первого пользователя
        self.user_1 = User.objects.create_user(
            email=self.email_1,
            password=self.password_1,
            role = self.role
        )
        # создание второго пользователя
        self.user_2 = User.objects.create_user(
            email=self.email_2,
            password=self.password_2,
            role = self.role
        )
        # создание третьего пользователя
        self.user_3 = User.objects.create_user(
            email=self.email_3,
            password=self.password_3,
            role = self.role
        )
        self.token_1 = Token.objects.create(user=self.user_1)
        self.token_2 = Token.objects.create(user=self.user_2)
        self.token_3 = Token.objects.create(user=self.user_3)

        # подгрузить документы из фикстур
        call_command('loaddata', 'fixtures/documents.json', verbosity=0)
        
        # получить корневую папку пользователя 1, созданную автоматически
        self.folder_root_1 = Folders.objects.get(owner=self.user_1)

        # получить корневую папку пользователя 2, созданную автоматически
        self.folder_root_2 = Folders.objects.get(owner=self.user_2)

        # создать папку 1 и вложить ее в корневую пользователя 1
        self.folder_1 = Folders(name='подпапка в корневой пользователя 1',
                                owner=self.user_1)
        Folders.objects.insert_node(self.folder_1, self.folder_root_1, save=True)

        # расшарить корневую папку пользователя 1 для пользователя 3
        self.folder_root_1.access_user.add(self.user_3)

        self.document = Documents.objects.get(id=1)
        

    def test_get_list_folders(self):
        """получить дерево папок пользователя 1"""
        response = client.get('/api/v1/folders/shema', HTTP_AUTHORIZATION='Token' + ' ' + self.token_1.key)
        result = json.loads(response.content)
        subfolder = result[0]['subfolders'][0]['name']
        self.assertEqual(subfolder, self.folder_1.name)
        self.assertEqual(response.status_code, 200)

    def test_get_list_share_folders(self):
        """получить расшареные папки"""
        # кому расшарено (пользователь 3)
        response = client.get('/api/v1/folders/share', HTTP_AUTHORIZATION='Token' + ' ' + self.token_3.key)
        result = json.loads(response.content)
        folder_name = result[0]['subfolders'][0]['name']
        self.assertEqual(folder_name, self.folder_1.name)
        self.assertEqual(response.status_code, 200)

        # кому не расшарено (пользователь 2)
        response = client.get('/api/v1/folders/share', HTTP_AUTHORIZATION='Token' + ' ' + self.token_2.key)
        self.assertEqual(response.content, b'[]')
        self.assertEqual(response.status_code, 200)

    def test_post_folders(self):
        """создать папку"""
        # в своем дереве
        data = {
            'id': self.folder_1.id,
            'type_content': 'folders',
            'parent': 'вновь созданная папка'
        }
        response = client.post('/api/v1/folders/create', data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_1.key)
        self.assertEqual(response.status_code, 201)

        # в чужом дереве
        data = {
            'id': self.folder_root_2.id,
            'type_content': 'folders',
            'parent': 'вновь созданная папка'
        }
        response = client.post('/api/v1/folders/create', data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_1.key)
        self.assertEqual(response.status_code, 403)
    
    def test_post_documents(self):
        """добавить в папку документ"""
        # в своем дереве
        data = {
            'id': self.folder_1.id,
            'type_content': 'documents',
            'id_content': self.document.id
        }
        response = client.post('/api/v1/folders/create', data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_1.key)
        self.assertEqual(response.status_code, 201)

        # в чужом дереве
        data = {
            'id': self.folder_root_2.id,
            'type_content': 'documents',
            'id_content': self.document
        }
        response = client.post('/api/v1/folders/create', data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_1.key)
        self.assertEqual(response.status_code, 403)
    

    def test_get_folders(self):
        """получить отдельную папку в дереве"""
        # владелец папки (пользователь 1)
        id = self.folder_1.id
        response = client.get('/api/v1/folders/' + str(id) + '/retrive', HTTP_AUTHORIZATION='Token' + ' ' + self.token_1.key)
        result = json.loads(response.content)
        folder_name = result['name']
        self.assertEqual(folder_name, self.folder_1.name)
        self.assertEqual(response.status_code, 200)

        # кому расшарено (пользователь 3)
        id = self.folder_1.id
        response = client.get('/api/v1/folders/' + str(id) + '/retrive', HTTP_AUTHORIZATION='Token' + ' ' + self.token_3.key)
        result = json.loads(response.content)
        folder_name = result['name']
        self.assertEqual(folder_name, self.folder_1.name)
        self.assertEqual(response.status_code, 200)

        # нет доступа (пользователь 2)
        id = self.folder_1.id
        response = client.get('/api/v1/folders/' + str(id) + '/retrive', HTTP_AUTHORIZATION='Token' + ' ' + self.token_2.key)
        self.assertEqual(response.status_code, 403)

    def test_put_folders(self):
        """изменить папку"""
        data = {
            'name': 'переименованная папка'
        }
        # владелец папки (пользователь 1)
        id = self.folder_1.id
        response = client.put('/api/v1/folders/' + str(id), data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_1.key)
        self.assertEqual(response.status_code, 200)
        
        # кому расшарено (пользователь 3)
        response = client.put('/api/v1/folders/' + str(id), data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_3.key)
        self.assertEqual(response.status_code, 403)

        # нет доступа (пользователь 2)
        response = client.put('/api/v1/folders/' + str(id), data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_2.key)
        self.assertEqual(response.status_code, 403)

    def test_patch_folders(self):
        """изменить папку"""
        data = {
            'name': 'переименованная папка'
        }
        # владелец папки (пользователь 1)
        id = self.folder_1.id
        response = client.patch('/api/v1/folders/' + str(id), data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_1.key)
        self.assertEqual(response.status_code, 200)
        
        # кому расшарено (пользователь 3)
        response = client.patch('/api/v1/folders/' + str(id), data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_3.key)
        self.assertEqual(response.status_code, 403)

        # нет доступа (пользователь 2)
        response = client.patch('/api/v1/folders/' + str(id), data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_2.key)
        self.assertEqual(response.status_code, 403)

    def test_delete_folders_owner(self):
        """удалить папку"""
        # владелец папки (пользователь 1)
        id = self.folder_1.id
        response = client.delete('/api/v1/folders/' + str(id), HTTP_AUTHORIZATION='Token' + ' ' + self.token_1.key)
        self.assertEqual(response.status_code, 204)
        
    def test_delete_folders_share(self):
        """удалить папку"""
        # кому расшарено (пользователь 3)
        id = self.folder_1.id
        response = client.delete('/api/v1/folders/' + str(id), HTTP_AUTHORIZATION='Token' + ' ' + self.token_3.key)
        self.assertEqual(response.status_code, 403)

    def test_delete_folders_not_access(self):
        """удалить папку"""
        # нет доступа (пользователь 2)
        id = self.folder_1.id
        response = client.delete('/api/v1/folders/' + str(id), HTTP_AUTHORIZATION='Token' + ' ' + self.token_2.key)
        self.assertEqual(response.status_code, 403)
