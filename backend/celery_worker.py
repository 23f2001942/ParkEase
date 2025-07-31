# backend/celery_wroker.py

from celery import Celery
from config import Config

celery = Celery(
    'parkease',
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND,
)
celery.conf.update(
    task_serializer   = 'json',
    result_serializer = 'json',
    accept_content    = ['json'],
    timezone          = 'UTC',
)
# autodiscover the tasks.py module
celery.autodiscover_tasks(['tasks'])

if __name__=='__main__':
    celery.start()
