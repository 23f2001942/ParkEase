# backend/celery_beat.py

from tasks import celery_app

if __name__ == '__main__':
    celery_app.beat_main()
