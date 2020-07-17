from django.db import models


class JournalRecord(models.Model):
    """ Запись в журнале импорта. """
    NORMDOC = 'normdoc'
    XML = 'xml'
    IMAGES = 'images'
    BERESTA = 'beresta'
    TYPE_CHOICES = (
        (NORMDOC, 'Нормдок'),
        (XML, 'XML'),
        (IMAGES, 'Изображения для XML'),
        (BERESTA, 'Береста')
    )

    INFO = 'info'
    ERROR = 'error'
    LEVEL_CHOISES = ((INFO, 'Инфо'), (ERROR, 'Ошибка'))

    type = models.CharField('Тип импорта', max_length=7, choices=TYPE_CHOICES)
    level = models.CharField('Уровень', max_length=5, choices=LEVEL_CHOISES)
    message = models.CharField('Сообщение', max_length=512)
    timestamp = models.DateTimeField('Время', auto_now_add=True)

    def __str__(self):
        return '[{}] {}'.fromat(self.level, self.message)

    class Meta:
        verbose_name = 'запись в журнале импорта'
        verbose_name_plural = 'Журнал импорта'


    @staticmethod
    def log(record_type, message, *args):
        """
        Пишет сообщение в журнал импорта.

        :param message: Сообщение.
        :param args: Данные для подстановки в message.
        """
        JournalRecord(
            type=record_type, level=JournalRecord.INFO, message=message % args
        ).save()


    @staticmethod
    def log_error(record_type, message, *args):
        """
        Пишет сообщение об ошибке в журнал импорта.

        :param message: Сообщение.
        :param args: Данные для подстановки в message.
        """
        JournalRecord(
            type=record_type, level=JournalRecord.ERROR, message=message % args
        ).save()
