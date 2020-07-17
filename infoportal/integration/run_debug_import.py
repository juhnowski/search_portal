"""
Дебажный скрипт для ручного запуска импорта.
На боевом сервере это должно делаться через Celery.
"""

import os
import sys
import argparse

import django
from django.conf import settings

parser = argparse.ArgumentParser(description='Запустить тестовый импорт.')
parser.add_argument(
    'type', choices=['normdoc', 'xml', 'beresta'], help='Тип импорта'
)
parser.add_argument(
    '--settings', default='settings.dev', help='Настройки Django'
)
parser.add_argument(
    '--permitted-docs',
    help='Дебажная быдло-фича, файл с ид документов для импорта из Нормдока'
)
args = parser.parse_args()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', args.settings)
django.setup()

from integration.normdoc import import_standards
from integration.xml_db import import_xml

if args.type == 'normdoc':
    permitted_docs = None
    if args.permitted_docs is not None:
        with open(args.permitted_docs) as f:
            permitted_docs = set([line.rstrip() for line in f])
    import_standards(
        settings.NORMDOC_HOST, settings.NORMDOC_PORT,
        settings.NORMDOC_USER, settings.NORMDOC_PASSWORD, permitted_docs
    )
elif args.type == 'xml':
    import_xml(
        settings.XML_DB_HOST, settings.XML_DB_DBNAME,
        settings.XML_DB_USER, settings.XML_DB_PASSWORD
    )
elif args.type == 'beresta':
    pass
