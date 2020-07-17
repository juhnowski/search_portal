"""
Структура данных Нормдока:
1. Корневая папка НСС:
   /app:company_home/cm:ecmc_document_space/cm:nd_gost_standards.
2. В ней папки стандартов.
3. В папке стандарта 2 узла: PDF и библиография. PDF может и не быть.
"""

import logging

from .alfresco_api import AlfrescoApi, AlfrescoError
from .models import JournalRecord
from documents.models import Documents

logger = logging.getLogger(__name__)

# Запрос для получения всех папок стандартов.
ALL_STANDARDS_QUERY = '/app:company_home/cm:ecmc_document_space/cm:nd_gost_standards/*'
# Запрос для получения содержимого папки стандарта.
STANDARD_INFO_QUERY = '/app:company_home/cm:ecmc_document_space/cm:nd_gost_standards/{name}/*'

BIB_TYPE = 'ecmcndgostst:nd_gost_standards'
PDF_TYPE = 'ecmccontent:document_origin'


def log(message, *args):
    """
    Пишет сообщение в logger и в журнал импорта.

    :param message: Сообщение.
    :param args: Данные для подстановки в message.
    """
    logger.info(message, *args)
    JournalRecord.log(JournalRecord.NORMDOC, message, *args)


def log_error(message, *args):
    """
    Пишет сообщение об ошибке в logger и в журнал импорта.

    :param message: Сообщение.
    :param args: Данные для подстановки в message.
    """
    logger.error(message, *args)
    JournalRecord.log_error(JournalRecord.NORMDOC, message, *args)


def get_date_decoder(property_name):
    """
    Вспомогательная функция для DECODERS.
    :param property_name: Название Alfreco-свойства.
    :return: Преобразователь даты, функция которая берёт заданное
             Alfreco-свойство и приводит его к нужному формату.
    """
    def decoder(id, properties, pdf_name, pdf_content):
        value = properties.get(property_name, None)
        return None if (value is None) else value.split('T')[0]
    return decoder


# Описывает как преобразовывать полученные данные в атрибуты нашей модели.
# Каждый декодер — это либо функция, либо tuple
# (название Alfreco-свойства и значение по умолчанию).
DECODERS = {
    'doc_sys_number': lambda id, props, pdf_name, pdf_content: id,
    'doc_status': ('ecmcnddoc:doc_status', None),
    'doc_kind': ('ecmcnddoc:doc_kind_cp_cm_name', None),
    'application_status': ('ecmcnddoc:application_status', None),
    'doc_mark': ('ecmcnddoc:doc_mark', None),
    'doc_full_mark': ('ecmcnddoc:doc_full_mark', None),
    'doc_name_ru': ('ecmcnddoc:doc_name_ru', None),
    'doc_name_en': ('ecmcnddoc:doc_name_en', None),
    'doc_annotation': ('ecmcnddoc:doc_annotation', ''),
    'doc_comment': ('ecmcnddoc:doc_comment', ''),
    'tk_rus': ('ecmctk:tk_author_cp_cm_title', ''),
    'org_author_name': ('ecmcnddoc:org_author_name', ''),
    'doc_reg_date': get_date_decoder('ecmcnddoc:doc_reg_date'),
    'doc_effective_date': get_date_decoder('ecmcnddoc:doc_effective_date'),
    'doc_restoration_date': lambda id, props, pdf_name, pdf_content: '2008-01-01', # TODO: WTF?
    'doc_assign_date': lambda id, props, pdf_name, pdf_content: '2008-01-02', # TODO: WTF?
    'doc_limit_date': lambda id, props, pdf_name, pdf_content: '2008-01-03', # TODO: WTF?
    'pdf_content_name': lambda id, props, pdf_name, pdf_content: pdf_name,
    'doc_pdf_content': lambda id, props, pdf_name, pdf_content: pdf_content
}


def decode_standard(standard, id, properties, pdf_name, pdf_content):
    """
    Конструирует экземпляр Documents из полученных от Alfresco данных
    при помощи DECODERS.

    :param standard: Экземпляр Documents, куда надо сложить данные.
    :param id: Ид узла в формате UUID.
    :param properties: Свойства узла.
    :param pdf_name: Название PDF-документа.
    :param pdf_content: Содержимое PDF-документа.
    """
    for attr, decoder in DECODERS.items():
        value = None
        if type(decoder) == tuple:
            value = properties.get(*decoder)
        elif callable(decoder):
            value = decoder(id, properties, pdf_name, pdf_content)

        # TODO: WTF?
        if attr == 'pdf_content_name' and value is None:
            value = ''
        # TODO: WTF?
        if attr == 'doc_effective_date' and value is None:
            value = '2008-01-04'
        # TODO: WTF?
        if attr == 'doc_reg_date':
            value = '2008-01-05'

        setattr(standard, attr, value)


def import_standard(alfresco, name, permitted_docs):
    """
    Импортирует конкретный стандарт.

    :param alfresco: Экземпляр AlfrescoApi.
    :param name: Название папки стандарта (не UUID).
    """
    name = 'cm:' + name.replace(' ', AlfrescoApi.WHITESPACE)
    data = alfresco.search(
        'PATH:"' + STANDARD_INFO_QUERY.format(name=name) + '"',
        properties_required=True
    )
    id = None
    properties = None
    pdf_name = None
    pdf_content = None
    for node in data['list']['entries']:
        if node['entry']['nodeType'] == BIB_TYPE:
            id = node['entry']['id']
            properties = node['entry']['properties']
        elif (node['entry']['nodeType'] == PDF_TYPE) and (pdf_name is None):
            try:
                pdf_content = alfresco.get_node_content(node['entry']['id'])
                pdf_name = node['entry']['name']
            except AlfrescoError:
                pass

    if (id is None) or (properties is None):
        log_error('Не скачалась папка стандарта %s. Пропускаем.', name)
        return

    # TODO: избавиться от этой дебажной дряни.
    if permitted_docs is not None:
        if properties['ecmcnddoc:doc_mark'] not in permitted_docs:
            logger.debug('Пропускаем %s.', properties['ecmcnddoc:doc_mark'])
            return

    # Создаём или обновляем документ в нашей БД.
    doc_mark = properties['ecmcnddoc:doc_mark']
    try:
        standard = Documents.objects.get(doc_sys_number=id)
        logger.info('Обновляем стандарт %s.', doc_mark)
    except Documents.DoesNotExist:
        standard = Documents()
        logger.info('Создаём новый стандарт %s.', doc_mark)
    decode_standard(standard, id, properties, pdf_name, pdf_content)
    standard.save()


def import_standards(host, port, user, password, permitted_docs=None):
    """
    Выполняет импорт из Нормдока.

    :param host: Хост.
    :param port: Порт, на котором работает Alfresco.
    :param user: Пользователь Нормдока.
    :param password: Пароль.
    """
    log('Запущен импорт из Нормдока.')
    try:
        alfresco = AlfrescoApi(host, port)
        alfresco.login(user, password)
        skip = 0
        while True:
            data = alfresco.search(
                'PATH:"' + ALL_STANDARDS_QUERY + '"',
                properties_required=False,
                skip=skip
            )
            for standard in data['list']['entries']:
                import_standard(
                    alfresco, standard['entry']['name'],
                    permitted_docs
                )
            skip += len(data['list']['entries'])
            if skip >= data['list']['pagination']['totalItems']:
                break
            if len(data['list']['entries']) == 0:
                break
        alfresco.logout()
        log('Импорт из Нормдока завершен в штатном режиме.')
    except AlfrescoError as e:
        log_error(str(e))
        log_error('Импорт из Нормдока не был завершен из-за ошибки.')
