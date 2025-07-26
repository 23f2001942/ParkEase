# backend/config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'you-will-never-guess-jwt')

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f"sqlite:///{os.path.join(basedir, 'parkease.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Celery (unused stubs)
    CELERY_BROKER_URL     = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')


