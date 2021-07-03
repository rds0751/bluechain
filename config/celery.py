from __future__ import absolute_import, unicode_literals

import os
import sys
import django

from celery import Celery

os.environ.setdefault('DJANGOS_SETTINGS_MODULE', 'jrindia.settings')

app = Celery('jrindia')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jrindia.settings.settings')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../jrindia')))
django.setup()
from django.conf import settings
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)