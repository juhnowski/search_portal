from django.contrib.auth import get_user_model

from django.test import TestCase
from django.utils import timezone

from rest_framework.authtoken.models import Token

from notes.models import Notes, Comments

User = get_user_model()


class NotesModelTest(TestCase):

    def createEntries(self):
        """создание записей в базе"""
        # данные пользователя
        self.email = 'test@example.com'
        self.password = 'test123'

        # создание пользователя
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password
        )
        self.token = Token.objects.create(user=self.user)

        # создаем заметку
        self.notes = Notes.objects.create(name='notes_1',
                                          owner=self.user,
                                          content='content_notes_1')

        # создаем комментарий
        self.comment = Comments.objects.create(owner=self.user,
                                                 content='content comment 1')
        # добавляем комментарий к заметке
        self.notes.comments.add(self.comment)

        return self.notes, self.comment

    def test_notes_creation(self):
        """проверка моделей"""
        create = self.createEntries()
        self.assertIsInstance(self.notes, Notes)
        self.assertEqual(create[0].__str__(), self.notes.name)

        self.assertIsInstance(self.comment, Comments)
        self.assertEqual(create[1].__str__(), self.comment.content)
