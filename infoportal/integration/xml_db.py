import os
import subprocess
import logging

import psycopg2

from .models import JournalRecord
from documents.models import Documents

logger = logging.getLogger(__name__)

QUERY = """
    SELECT reference, content FROM document, document_version
    WHERE (document.current_version_id = document_version.id)
"""
# Скрипт для XSTL-преобразования.
XSLT_PATH = os.path.join(
    os.path.dirname(__file__),
    'xml-processing/isosts2gosthtml_standalone_pnst.xsl'
)
# Команда для XSLT-преобразования.
COMMAND = 'saxonb-xslt -ext:on -s:- -xsl:' + XSLT_PATH


def log(message, *args):
    """
    Пишет сообщение в logger и в журнал импорта.

    :param message: Сообщение.
    :param args: Данные для подстановки в message.
    """
    logger.info(message, *args)
    JournalRecord.log(JournalRecord.XML, message, *args)


def log_error(message, *args):
    """
    Пишет сообщение об ошибке в logger и в журнал импорта.

    :param message: Сообщение.
    :param args: Данные для подстановки в message.
    """
    logger.error(message, *args)
    JournalRecord.log_error(JournalRecord.XML, message, *args)


class XsltException(Exception):
    def __init__(self):
        super(XsltException, self).__init__('XSLT fail')


def decode_xml(xml):
    """
    Прегоняет XML (из БД с XML) в HTML посредством XSLT-преобразования.

    :param xml: XML в виде строки.
    :return: HTML в виде строки.
    """
    try:
        proc = subprocess.Popen(
            COMMAND.split(' '), stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    except FileNotFoundError:
        logger.error(
            'Не удалось запустить команду «%s». Пакет установлен?', COMMAND
        )
        raise XsltException()
    out, err = proc.communicate(input=xml.encode())
    if proc.returncode != 0:
        logger.error(
            'Получен код %d от команды «%s». %s',
            proc.returncode, COMMAND, err.decode('utf-8').strip()
        )
        raise XsltException()
    return out.decode('utf-8')


def decode_doc_mark(doc_mark):
    """
    В БД с XML обозначения документов хранятся в каком-то странном виде.
    Для сопоставления с БД Нормдока их надо привести в норму.

    :param doc_mark: Обозначение документа из БД с XML.
    :return: Нормальное обозначение документа.
    """
    FIXES = [
        (' (ru)', ''),
        ('\n', ' '),
        ('\u2028', ' '),
        ('―', '-'),
        ('—', '-'),
        ('- ', '-'),
        ('  ', ' '),
        ('       ', ' ')
    ]
    for fix in FIXES:
        doc_mark = doc_mark.replace(*fix)
    return doc_mark.strip()


def import_xml(host, dbname, user, password):
    """
    Выполняет импорт из БД с XML.
    """
    log('Запущен импорт из БД c XML.')
    try:
        conn = psycopg2.connect(
            host=host, dbname=dbname, user=user, password=password
        )
    except psycopg2.Error:
        log_error('Не удалось подключиться к серверу PostgreSQL.')
        log_error('Импорт из Нормдока не был завершен из-за ошибки.')
        return

    try:
        cursor = conn.cursor()
        cursor.execute(QUERY)
        for row in cursor:
            doc_mark, xml = row
            try:
                doc = Documents.objects.get(doc_mark=decode_doc_mark(doc_mark))
                doc.doc_html_content = decode_xml(xml)
                doc.save()
                logger.info('Обновлен XML для стандарта %s.', doc.doc_mark)
            except Documents.DoesNotExist:
                log_error('Не найден стандарт, соответствующий %s.', doc_mark)
            except XsltException:
                log_error('Ошибка при XSLT-преобразовании %s.', doc_mark)
        cursor.close()
        conn.close()
        log('Импорт из БД с XML завершен в штатном режиме.')
    except psycopg2.Error as e:
        log_error('Ошибка в модуле psycopg2: «%s».', e.pgerror)
        log_error('Импорт из Нормдока не был завершен из-за ошибки.')
