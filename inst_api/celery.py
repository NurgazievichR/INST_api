from __future__ import absolute_import

import os
from time import sleep

from celery import Celery

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inst_api.settings')


app = Celery('inst_api')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    for i in range(10):
        print('it works')
        sleep(10)