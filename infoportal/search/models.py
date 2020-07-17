import logging

from django.db import models

logger = logging.getLogger('django')


class SearchOptions(models.Model):
    document_type = models.TextField('Вид документа', null=True)
    brief_document_description = models.TextField('Краткое Обозначение документа', null=True)
    name_ru = models.TextField('Наименование на русском языке', null=True)
    name_en = models.TextField('Наименование на английском языке', null=True)
    abstract = models.TextField('Аннотация(Область применения)', null=True)
    note = models.TextField('Примечание', null=True)
    full_designation_of_the_document = models.TextField('Полное обозначение документа', null=True)
    document_status = models.TextField('Статус документа', null=True)
    document_approval_date = models.TextField('Дата утверждения документа', null=True)
    date_of_adoption = models.TextField('Дата принятия', null=True)
    effective_date = models.TextField('Дата введения в действие', null=True)
    recover_date = models.TextField('Дата восстановления действия', null=True)
    okved = models.TextField('ОКВЭД', null=True)
    oks = models.TextField('Код ОКС', null=True)
    tk = models.TextField('ТК России', null=True)
    mtk = models.TextField('МТК, разработавший документ', null=True)
    keywords = models.TextField('Ключевые слова', null=True)

    def __str__(self):
        result = []
        if self.document_type:
            result.append(f'{self.document_type}')
        if self.brief_document_description:
            result.append(f'{self.brief_document_description}')
        if self.name_ru:
            result.append(f'{self.name_ru}')
        if self.name_en:
            result.append(f'{self.name_en}')
        if self.abstract:
            result.append(f'{self.abstract}')
        if self.note:
            result.append(f'{self.note}')
        if self.full_designation_of_the_document:
            result.append(f'{self.full_designation_of_the_document}')
        if self.document_status:
            result.append(f'{self.document_status}')
        if self.document_approval_date:
            result.append(f'{self.document_approval_date}')
        if self.date_of_adoption:
            result.append(f'{self.date_of_adoption}')
        if self.effective_date:
            result.append(f'{self.effective_date}')
        if self.recover_date:
            result.append(f'{self.recover_date}')
        if self.okved:
            result.append(f'{self.okved}')
        if self.oks:
            result.append(f'{self.oks}')
        if self.tk:
            result.append(f'{self.tk}')
        if self.mtk:
            result.append(f'{self.mtk}')
        if self.keywords:
            result.append(f'{self.keywords}')

        return result.__str__()

    class Meta:
        verbose_name = 'SearchOptions (варианты расширенного поиска)'
        verbose_name_plural = 'SearchOptions (варианты расширенного поиска)'


class Search(models.Model):
    search_text = models.TextField('Поисковая строка', null=True)
    search_options = models.ForeignKey(SearchOptions, on_delete=models.DO_NOTHING, null=True)
    page_size = models.IntegerField('Количество записей на странице', null=True)

    def __str__(self):
        return f'search_text={self.search_text} +  self.search_options={self.search_options}'

    class Meta:
        verbose_name = 'Search (Поисковая строка)'
        verbose_name_plural = 'Searches (Поисковые строки)'


class SearchHistory(models.Model):
    search = models.ForeignKey(Search, on_delete=models.DO_NOTHING)
    userid = models.IntegerField('id пользователя')

    def __str__(self):
        return f'userid={self.userid} search={self.search}'

    class Meta:
        verbose_name = 'SearchHistory (История поиска)'
        verbose_name_plural = 'SearchHistories (Истории поисков)'


class AutoCompletion(models.Model):
    search_text = models.TextField('Поисковая строка')
    page_size = models.IntegerField('Количество записей на странице')

    def __str__(self):
        return f'search_text={self.search_text}'

    class Meta:
        verbose_name = ' Auto Completion (Автодополнение)'
        verbose_name_plural = 'Auto Completions (Автодополнения)'
