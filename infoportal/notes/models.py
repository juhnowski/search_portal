from django.db import models
from django.contrib.auth import get_user_model

from documents.models import Documents


CustomUserModel = get_user_model()


class Comments(models.Model):
    owner = models.ForeignKey(CustomUserModel,
                             verbose_name='Пользователь',
                             on_delete=models.CASCADE)
    content = models.TextField('Текст комментария')
    created = models.DateTimeField('Создан', auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии к заметкам'


class Notes(models.Model):
    name = models.CharField('Название', max_length=255)
    owner = models.ForeignKey(CustomUserModel,
                             verbose_name='Пользователь',
                             on_delete=models.CASCADE)
    content = models.TextField('Текст заметки')
    access_user = models.ManyToManyField(CustomUserModel,
                                         related_name='access_user_notes',
                                         verbose_name='Пользователи',
                                         blank=True)
    comments = models.ManyToManyField(Comments,
                                      verbose_name='Комментарий',
                                      blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'заметка'
        verbose_name_plural = 'Заметки пользователя'
