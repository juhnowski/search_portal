from django.db import models
from django.utils import timezone


class DocumentsAnalytics(models.Model):
    date = models.DateField(verbose_name='дата', default=timezone.now)

    total_docs = models.IntegerField(verbose_name='Всего документов', default=0)

    gost_r = models.IntegerField(verbose_name='ГОСТ Р', default=0)
    pnst = models.IntegerField(verbose_name='ПНСТ', default=0)
    gost = models.IntegerField(verbose_name='ГОСТ', default=0)
    pr = models.IntegerField(verbose_name='ПР', default=0)
    r = models.IntegerField(verbose_name='Р', default=0)
    pmg = models.IntegerField(verbose_name='ПМГ', default=0)
    rmg = models.IntegerField(verbose_name='РМГ', default=0)
    its = models.IntegerField(verbose_name='ИТС', default=0)
    ok = models.IntegerField(verbose_name='ОК', default=0)
    sp = models.IntegerField(verbose_name='СП', default=0)
    iso = models.IntegerField(verbose_name='ИСО', default=0)
    mek = models.IntegerField(verbose_name='МЭК', default=0)
    russian_docs = models.IntegerField(verbose_name='Документов РФ', default=0)
    foreign_docs = models.IntegerField(verbose_name='Международных документов', default=0)

    def __str__(self):
        return str(self.total_docs)

    class Meta:
        verbose_name = 'Статистика по документам'
        verbose_name_plural = 'Статистика по документам'


class Analytics(models.Model):
    date = models.DateField(verbose_name='дата', default=timezone.now)

    documents = models.OneToOneField(
        DocumentsAnalytics, on_delete=models.CASCADE, verbose_name='Статистика по документам'
    )

    users = models.IntegerField(verbose_name='Всего пользователей', default=0)
    companies = models.IntegerField(verbose_name='Всего компаний', default=0)
    notes = models.IntegerField(verbose_name='Всего заметок', default=0)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'
