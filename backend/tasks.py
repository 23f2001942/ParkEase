# backend/tasks.py

from celery import Celery
from config import Config

celery_app = Celery('parkease',
                    broker=Config.CELERY_BROKER_URL,
                    backend=Config.CELERY_RESULT_BACKEND)