import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')
app = Celery('infoportal')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()
