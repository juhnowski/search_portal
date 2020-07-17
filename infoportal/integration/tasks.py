"""
Задачи Celery.
"""
import logging

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from django.conf import settings

from .normdoc import import_standards
from .xml_db import import_xml
from .beresta import update_notifications

logger = logging.getLogger(__name__)


@periodic_task(run_every=crontab(minute=0, hour='2'), ignore_result=True)
def synchronize_with_normdoc():
    logger.info('Запущен импорт из Нормдока')
    import_standards(
        settings.NORMDOC_HOST, settings.NORMDOC_PORT,
        settings.NORMDOC_USER, settings.NORMDOC_PASSWORD
    )


@periodic_task(run_every=crontab(minute=0, hour='4'), ignore_result=True)
def synchronize_with_xml_db():
    logger.info('Запущен импорт из БД с XML')
    import_xml(
        settings.XML_DB_HOST, settings.XML_DB_DBNAME,
        settings.XML_DB_USER, settings.XML_DB_PASSWORD
    )


@periodic_task(run_every=crontab(minute=0, hour='6'), ignore_result=True)
def synchronize_with_beresta():
    logger.info('Запущен импорт из Бересты')
    update_notifications()
