import json

from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from notes.models import Notes, Comments
from folders.models import Folders

User = get_user_model()

client = APIClient()

class NotesTestCase(APITestCase):

    def setUp(self):
        # данные первого пользователя
        self.email_1 = 'test_1@example.com'
        self.password_1 = 'test123'

        # данные второго пользователя
        self.email_2 = 'test_2@example.com'
        self.password_2 = 'test321'

        # данные третьего пользователя
        self.email_3 = 'test_3@example.com'
        self.password_3 = 'test567'

        # создание первого пользователя
        self.user_1 = User.objects.create_user(
            email=self.email_1,
            password=self.password_1,
        )
        # создание второго пользователя
        self.user_2 = User.objects.create_user(
            email=self.email_2,
            password=self.password_2,
        )
        # создание третьего пользователя
        self.user_3 = User.objects.create_user(
            email=self.email_3,
            password=self.password_3,
        )
        self.token_1 = Token.objects.create(user=self.user_1)
        self.token_2 = Token.objects.create(user=self.user_2)
        self.token_3 = Token.objects.create(user=self.user_3)

        # создаем заметку 1 от пользователя 1
        self.notes = Notes.objects.create(name='notes_1',
                                          owner=self.user_1,
                                          content='content_notes_1')
        # расшариваем заметку 1 для пользователя 2
        self.notes.access_user.add(self.user_2)

        # создаем комментарий_1 от пользователя 1
        self.comment_1 = Comments.objects.create(owner=self.user_1,
                                                 content='content comment 1')
        # добавляем комментарий_1 к заметке
        self.notes.comments.add(self.comment_1)

        # получить корневую папку пользователя 1, созданную автоматически
        folder_root = Folders.objects.get(owner=self.user_1)

        # создать папку 1 и вложить ее в корневую
        self.folder_1 = Folders(name='subfolder in root folder of the user 1',
                                owner=self.user_1)
        Folders.objects.insert_node(self.folder_1, folder_root, save=True)

        # создать заметку 2 от пользователя 1
        self.notes_2 = Notes.objects.create(name='notes_2',
                                            owner=self.user_1,
                                            content='content_notes_2')

        # добавить заметку 2 в папку 1
        self.folder_1.notes.add(self.notes_2)

        # расшарить корневую папку пользователя 1 для пользователя 3
        folder_root.access_user.add(self.user_3)


    def test_get_list_notes(self):
        """получить список собственных заметок пользователя"""
        response = client.get('/api/v1/notes/', HTTP_AUTHORIZATION='Token' + ' ' + self.token_1.key)
        result = json.loads(response.content)
        name_notes_1 = result['results'][0]['name']
        self.assertEqual(name_notes_1, self.notes.name)
        self.assertEqual(response.status_code, 200)

    def test_post_notes(self):
        """создать заметку"""
        data = {
            'name': 'notes_name',
            'content': 'notes_content',
            'access_user': self.user_2.id
        }
        response = client.post('/api/v1/notes/create', data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_1.key)
        self.assertEqual(response.status_code, 201)

    def test_get_list_notes_other(self):
        """получить список расшареных заметок для второго пользователя"""
        response = client.get('/api/v1/notes/other', HTTP_AUTHORIZATION='Token' + ' ' + self.token_2.key)
        # print (response.content)
        result = json.loads(response.content)
        name_notes_1 = result['results'][0]['name']
        self.assertEqual(name_notes_1, self.notes.name)
        self.assertEqual(response.status_code, 200)

    def test_get_notes(self):
        """получить отдельную заметку"""
        # владельцем заметки
        response = client.get('/api/v1/notes/1', HTTP_AUTHORIZATION='Token' + ' ' + self.token_1.key)
        result = json.loads(response.content)
        name_notes_1 = result['name']
        self.assertEqual(name_notes_1, self.notes.name)
        self.assertEqual(response.status_code, 200)

        # кому расшарена заметка
        response = client.get('/api/v1/notes/1', HTTP_AUTHORIZATION='Token' + ' ' + self.token_2.key)
        result = json.loads(response.content)
        name_notes_1 = result['name']
        self.assertEqual(name_notes_1, self.notes.name)
        self.assertEqual(response.status_code, 200)

        # не имеющим доступ
        response = client.get('/api/v1/notes/1', HTTP_AUTHORIZATION='Token' + ' ' + self.token_3.key)
        self.assertEqual(response.status_code, 403)

    def test_put_notes(self):
        """изменить отдельную заметку"""
        data = {
            'name': 'notes_name_new',
            'content': 'notes_content',
            'access_user': self.user_2.id
        }
        # пользователь 1 (владелец)
        response = client.put('/api/v1/notes/1', data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_1.key)
        self.assertEqual(response.status_code, 200)

        # пользователь 2 (расшарено)
        response = client.put('/api/v1/notes/1', data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_2.key)
        self.assertEqual(response.status_code, 403)

        # пользователь 3 (не имеет доступа)
        response = client.put('/api/v1/notes/1', data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_3.key)
        self.assertEqual(response.status_code, 403)

    def test_patch_notes(self):
        """изменить отдельную заметку"""
        data = {
            'name': 'notes_name_new',
            'content': 'notes_content',
            'access_user': self.user_2.id
        }
        # пользователь 1 (владелец)
        response = client.patch('/api/v1/notes/1', data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_1.key)
        self.assertEqual(response.status_code, 200)

        # пользователь 2 (расшарено)
        response = client.patch('/api/v1/notes/1', data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_2.key)
        self.assertEqual(response.status_code, 403)

        # пользователь 3 (не имеет доступа)
        response = client.patch('/api/v1/notes/1', data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_3.key)
        self.assertEqual(response.status_code, 403)

    def test_delete_notes_owner(self):
        """удалить отдельную заметку"""
        # пользователь 1 (владелец)
        response = client.delete('/api/v1/notes/1', HTTP_AUTHORIZATION='Token' + ' ' + self.token_1.key)
        self.assertEqual(response.status_code, 204)

    def test_delete_notes_share(self):
        """удалить отдельную заметку"""
        # пользователь 2 (расшарено)
        response = client.delete('/api/v1/notes/1', HTTP_AUTHORIZATION='Token' + ' ' + self.token_2.key)
        self.assertEqual(response.status_code, 403)

    def test_delete_notes_not_access(self):
        """удалить отдельную заметку"""
        # пользователь 3 (не имеет доступа)
        response = client.delete('/api/v1/notes/1', HTTP_AUTHORIZATION='Token' + ' ' + self.token_3.key)
        self.assertEqual(response.status_code, 403)

    def test_get_list_comments(self):
        """получить список комментариев к заметке 1"""
        # для пользователя 1 (владельца)
        response = client.get('/api/v1/notes/1/comments', HTTP_AUTHORIZATION='Token' + ' ' + self.token_1.key)
        result = json.loads(response.content)
        content_comment_1 = result['results'][0]['content']
        self.assertEqual(content_comment_1, self.comment_1.content)
        self.assertEqual(response.status_code, 200)

        # для пользователя 2 (расшарено)
        response = client.get('/api/v1/notes/1/comments', HTTP_AUTHORIZATION='Token' + ' ' + self.token_2.key)
        result = json.loads(response.content)
        content_comment_1 = result['results'][0]['content']
        self.assertEqual(content_comment_1, self.comment_1.content)
        self.assertEqual(response.status_code, 200)

        # для пользователя 3 (не имеет доступа)
        response = client.get('/api/v1/notes/1/comments', HTTP_AUTHORIZATION='Token' + ' ' + self.token_3.key)
        self.assertEqual(response.status_code, 403)

    def test_post_comments(self):
        """создать комментарий"""
        data = {
            'content': 'comment content'
        }
        # для пользователя 1 (владельца)
        response = client.post('/api/v1/notes/1/commentcreate', data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_1.key)
        self.assertEqual(response.status_code, 200)

        # для пользователя (расшарено)
        response = client.post('/api/v1/notes/1/commentcreate', data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_2.key)
        self.assertEqual(response.status_code, 200)

        # для пользователя 3 (не имеет доступа)
        response = client.post('/api/v1/notes/1/commentcreate', data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_3.key)
        self.assertEqual(response.status_code, 403)

    def test_put_comments(self):
        """изменить комментарий"""
        data = {
            'content': 'comment content 2'
        }
        # для пользователя 1 (владельца)
        response = client.put('/api/v1/notes/comments/1', data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_1.key)
        self.assertEqual(response.status_code, 200)

        # для пользователя (расшарено)
        response = client.put('/api/v1/notes/comments/1', data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_2.key)
        self.assertEqual(response.status_code, 403)

        # для пользователя 3 (не имеет доступа)
        response = client.put('/api/v1/notes/comments/1', data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_3.key)
        self.assertEqual(response.status_code, 403)

    def test_patch_comments(self):
        """изменить комментарий"""
        data = {
            'content': 'comment content 2'
        }
        # для пользователя 1 (владельца)
        response = client.patch('/api/v1/notes/comments/1', data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_1.key)
        self.assertEqual(response.status_code, 200)

        # для пользователя (расшарено)
        response = client.patch('/api/v1/notes/comments/1', data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_2.key)
        self.assertEqual(response.status_code, 403)

        # для пользователя 3 (не имеет доступа)
        response = client.patch('/api/v1/notes/comments/1', data, HTTP_AUTHORIZATION='Token' + ' ' + self.token_3.key)
        self.assertEqual(response.status_code, 403)

    def test_delete_comments_owner(self):
        """удалить комментарий"""
        # для пользователя 1 (владельца)
        response = client.delete('/api/v1/notes/comments/1', HTTP_AUTHORIZATION='Token' + ' ' + self.token_1.key)
        self.assertEqual(response.status_code, 204)

    def test_delete_comments_share(self):
        """удалить комментарий"""
        # для пользователя 2 (расшарено)
        response = client.delete('/api/v1/notes/comments/1', HTTP_AUTHORIZATION='Token' + ' ' + self.token_2.key)
        self.assertEqual(response.status_code, 403)

    def test_delete_comments_not_access(self):
        """удалить комментарий"""
        # для пользователя 3 (не имеет доступа)
        response = client.delete('/api/v1/notes/comments/1', HTTP_AUTHORIZATION='Token' + ' ' + self.token_3.key)
        self.assertEqual(response.status_code, 403)

    def test_get_folder_notes(self):
        """получить отдельную заметку в папке"""
        # для пользователя 3 (расшарено через папку)
        response = client.get('/api/v1/notes/2', HTTP_AUTHORIZATION='Token' + ' ' + self.token_3.key)
        result = json.loads(response.content)
        name_notes_2 = result['name']
        self.assertEqual(name_notes_2, self.notes_2.name)
        self.assertEqual(response.status_code, 200)

        # для пользователя 2 (не имеет доступа)
        response = client.get('/api/v1/notes/2', HTTP_AUTHORIZATION='Token' + ' ' + self.token_2.key)
        self.assertEqual(response.status_code, 403)

