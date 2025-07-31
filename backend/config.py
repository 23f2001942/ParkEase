import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Flask
    SECRET_KEY       = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    JWT_SECRET_KEY   = os.environ.get('JWT_SECRET_KEY', 'you-will-never-guess-jwt')

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f"sqlite:///{os.path.join(basedir, 'parkease.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CORS
    CORS_HEADERS = 'Content-Type'

    # Redis cache
    CACHE_TYPE            = "RedisCache"   
    CACHE_REDIS_URL       = os.environ.get("REDIS_URL", "redis://localhost:6379/1")
    CACHE_DEFAULT_TIMEOUT = 60    

    # Celery broker/backend
    CELERY_BROKER_URL     = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0') 
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0') 

    # Flask-Mail (for reminders & reports)
    MAIL_SERVER        = os.environ.get('MAIL_SERVER', 'localhost')  
    MAIL_PORT          = int(os.environ.get('MAIL_PORT', 25))        
    MAIL_USE_TLS       = os.environ.get('MAIL_USE_TLS', 'false').lower() in ('true','1')  
    MAIL_USE_SSL       = os.environ.get('MAIL_USE_SSL', 'false').lower() in ('true','1')  
    MAIL_USERNAME      = os.environ.get('MAIL_USERNAME')    
    MAIL_PASSWORD      = os.environ.get('MAIL_PASSWORD')        
    MAIL_DEFAULT_SENDER= os.environ.get('MAIL_DEFAULT_SENDER','noreply@parkease.com')

    # Exports
    EXPORT_FOLDER = os.path.join(basedir, 'exports')  
    os.makedirs(EXPORT_FOLDER, exist_ok=True)  
