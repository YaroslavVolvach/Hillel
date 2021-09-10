import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hillel.settings')

app = Celery('hillel')

# from django.conf import settings
# CELERY_

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# celery -A proj.tasks worker --loglevel=info --pool=solo
# celery -A hillel beat

# celery -A proj beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler