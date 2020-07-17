from django.db import models
from django.contrib.auth import get_user_model

from mptt.models import MPTTModel, TreeForeignKey

from documents.models import Documents
from notes.models import Notes

CustomUserModel = get_user_model()


class Folders(MPTTModel):
    name = models.CharField('Наименование', max_length=255)
    parent = TreeForeignKey('self',
                            null=True,
                            blank=True,
                            related_name='parent_folder',
                            verbose_name='Вышестоящая папка',
                            db_index=True,
                            on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUserModel,
                              on_delete=models.CASCADE,
                              verbose_name='Владелец')
    access_user = models.ManyToManyField(CustomUserModel,
                          related_name='access_user_folder',
                          verbose_name='Пользователи, которым расшарен доступ',
                          blank=True)
    documents = models.ManyToManyField(Documents, verbose_name='Документы',
                                       blank=True)
    notes = models.ManyToManyField(Notes, verbose_name='Заметки',
                                   blank=True)

    def __str__(self):
        return self.name

    class MPTTMeta:
        db_table = 'folders'
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Папка'
        verbose_name_plural = 'Папки'
