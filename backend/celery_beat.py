# backend/celery_beat.py

from celery_worker import celery
from celery.schedules import crontab

celery.conf.beat_schedule = {
    'daily-reminders': {
        'task': 'tasks.send_daily_reminders',  
        'schedule': 24*3600,
    },
    'monthly-reports': {
        'task': 'tasks.send_monthly_reports',   
        'schedule': crontab(day_of_month=1, hour=0, minute=0),
    },
}

if __name__=='__main__':
    celery.beat()

