from django.db import models
from django.contrib.auth import get_user_model

CustomUserModel = get_user_model()


STATUS_CHOICES = (
    ('actual', 'Действует'),
    ('cancel', 'Отменен'),
    ('replace', 'Заменен'),
    ('approve', 'Принят'),
    ('stop_use_rf', 'Прекратил применение на территории РФ'),
    ('expired', 'Срок действия истек'),
    ('not_actual', 'Не действует'),
    ('repealed', 'Утратил силу'),
    ('removed', 'Удален'),
)


APPLICATIONS_CHOICES = (
    ('mandatory', 'Обязательное'),
    ('voluntary', 'Добровольное'),
    ('for_rf', 'Для применения в РФ'),
)


class CISCountries(models.Model):
    name = models.CharField('Название страны', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'название страны СНГ'
        verbose_name_plural = 'Названия стран СНГ'


class CodeOKVED(models.Model):
    code = models.CharField('Код ОКВЭД', max_length=255)
    title = models.TextField('Наименование')
    description = models.TextField('Описание применения кода')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Код ОКВЭД'
        verbose_name_plural = 'Коды ОКВЭД'


class CodeOKS(models.Model):
    code = models.CharField('Код ОКС', max_length=255)
    title = models.TextField('Наименование')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Код ОКС'
        verbose_name_plural = 'Коды ОКС'


class CodeOKPD(models.Model):
    code = models.CharField('Код ОКПД', max_length=255)
    title = models.TextField('Наименование')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Код ОКПД'
        verbose_name_plural = 'Коды ОКПД'


class OriginLanguage(models.Model):
    language = models.CharField('Язык', max_length=255)

    def __str__(self):
        return self.language

    class Meta:
        verbose_name = 'Язык оригинала'
        verbose_name_plural = 'Языки оригинала'


class Documents(models.Model):
    doc_kind = models.CharField('Вид документа', max_length=255)
    doc_mark = models.CharField('Обозначение документа (краткое)',
                                max_length=255)
    doc_name_ru = models.CharField('Наименование на русском языке',
                                   max_length=512)
    doc_name_en = models.CharField('Наименование на английском языке',
                                   max_length=512)
    doc_annotation = models.TextField('Аннотация (область применения)')
    doc_comment = models.TextField('Примечание')
    doc_sys_number = models.CharField('Системный номер документа',
                                      max_length=64)
    doc_full_mark = models.TextField('Полное обозначение документа')
    doc_status = models.CharField('Статус документа',
                                  max_length=11,
                                  choices=STATUS_CHOICES)
    application_status = models.CharField('Статус применения',
                                          max_length=9,
                                          choices=APPLICATIONS_CHOICES)
    doc_reg_date = models.DateField('Дата утверждения документа')
    doc_limit_date = models.DateField('Дата ограничения срока действия')
    doc_on_rf_use = models.NullBooleanField('На территории РФ пользоваться',
                                            default=None)
    classifier_pns = models.CharField('Шифр темы ПНС', max_length=255)
    doc_assign_org = models.CharField('Документ принят (организация)',
                                      max_length=255,
                                      blank=True)
    doc_assign_date = models.DateField('Дата принятия')
    classifier_enterd_countries = models.ManyToManyField(CISCountries,
                                    verbose_name='Присоединившиеся страны СНГ',
                                    related_name='ciscountries')
    doc_reg_text = models.CharField('Номер приказа', max_length=255)
    doc_effective_date = models.DateField('Дата введения в действие')
    doc_restoration_date = models.DateField('Дата восстановления действия')
    doc_enter_org = models.CharField('Документ внесен (организация)',
                                     max_length=255,
                                     blank=True)
    classifier_okved = models.ManyToManyField(CodeOKVED,
                                              verbose_name='Код ОКВЭД')
    classifier_oks = models.ManyToManyField(CodeOKS,
                                            verbose_name='Код ОКС/МКС',
                                            blank=True)
    classifier_okp = models.ManyToManyField(CodeOKPD,
                                            verbose_name='Код ОКПД',
                                            blank=True)
    tk_rus = models.CharField('ТК России', max_length=64)
    org_author_name = models.CharField('Организация-разработчик',
                                       max_length=1024)
    mtk_dev = models.CharField('МТК разработавший документ', max_length=255)
    keywords = models.TextField('Ключевые слова')
    doc_annotation_ru = models.TextField('Аннотация на русском языке')
    doc_origin_language = models.ManyToManyField(OriginLanguage,
                                           verbose_name='Язык оригинала')
    contains_in_npa_links = models.BooleanField('Содержатся в ссылках в НПА',
                                                 default=False)
    cancel_in_part = models.TextField('Отменен в части', blank=True)
    doc_o_zsh = models.CharField('Обозначение заменяющего', max_length=255,
                                  blank=True)
    doc_o_zgo_vch = models.CharField('Обозначение заменяющего в части',
                                     max_length=255,
                                     blank=True)
    doc_o_zgo = models.CharField('Обозначение заменяемого',
                                  max_length=255,
                                  blank=True)
    doc_o_zsh_vch = models.CharField('Обозначение заменяемого в части',
                                      max_length=255,
                                      blank=True)
    doc_supplemented = models.CharField('Обозначение дополняемого',
                                        max_length=255,
                                        blank=True)
    doc_supplementing = models.CharField('Обозначение дополняющего',
                                          max_length=255,
                                          blank=True)
    related_documents = models.ManyToManyField('self',
                               verbose_name='Документы, на которые ссылается '
                                             'настоящий документ',
                               related_name='documents+',
                               symmetrical=False,
                               blank=True,)
    doc_outside_system = models.TextField('Документы вне системы, на которые '
                                          'ссылается настоящий документ',
                                          blank=True)
    doc_html_content = models.TextField('HTML контент документа', blank=True)
    doc_image_content = models.BinaryField('Документ в виде картинки',
                                           null=True,
                                           blank=True)
    image_contemt_name = models.CharField('Наименование файла картинки',
                                           max_length=255,
                                           blank=True)
    doc_pdf_content = models.BinaryField('Документ в виде PDF',
                                     null=True,
                                     blank=True)
    pdf_content_name = models.CharField('Наименование файла PDF',
                                        max_length=255,
                                        blank=True)
    doc_changes = models.TextField('Изменения и правки', blank=True)
    has_document_case = models.TextField('Дело документа', blank=True)
    # doc_rating = models.FloatField('Оценка', default=0)

    @property
    def doc_rating(self):
        return self.ratings.aggregate(doc_rating=models.Avg('value'))['doc_rating']

    def __str__(self):
        return self.doc_name_ru

    class Meta:
        verbose_name = 'документ'
        verbose_name_plural = 'Документы'


class TextSetings(models.Model):
    position = models.CharField('Позиция', max_length=255)
    color = models.CharField('Цвет', max_length=255)
    start = models.PositiveIntegerField('Начало')
    end = models.PositiveIntegerField('Конец')

    def __str__(self):
        return self.position

    class Meta:
        verbose_name = 'настройки закладок'
        verbose_name_plural = 'Настройки закладок'


class Ratings(models.Model):
    value = models.IntegerField('Оценка')
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, blank=True, null=True)
    document = models.ForeignKey(Documents, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self):
        return str(self.user) + ': ' + str(self.value)

    class Meta:
        unique_together = ['user', 'document']
        verbose_name = 'оценка'
        verbose_name_plural = 'оценки'


class Position(models.Model):
    right = models.CharField('Справа', max_length=255)
    top = models.CharField('Сверху', max_length=255)

    def __str__(self):
        return '%s %s' % (self.right, self.top)

    class Meta:
        verbose_name = 'позиция'
        verbose_name_plural = 'Позиции'
    

class Comments(models.Model):
    elem = models.CharField('Элемент', max_length=255)
    place = models.CharField('Место', max_length=255, blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    text = models.TextField('Текст')
    visual = models.BooleanField('Отображение')

    def __str__(self):
        return self.elem

    class Meta:
        verbose_name = 'комментарии к документу'
        verbose_name_plural = 'Комментарии к документу'


class DocumentsNotice(models.Model):
    text_settings = models.ManyToManyField(TextSetings, blank=True)
    comments = models.ManyToManyField(Comments, blank=True)
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    document = models.ForeignKey(Documents, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'данные к документу'
        verbose_name_plural = 'Данные к документу'
        constraints = [
            models.UniqueConstraint(fields=['user', 'document'], name='unique_notice_document')
        ]
