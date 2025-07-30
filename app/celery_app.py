import os
from celery import Celery
from celery.schedules import crontab
# from dotenv import load_dotenv


# load_dotenv()


redis_broker_url = os.getenv('REDIS_BROKER_URL', 'redis://localhost:6379/0')
redis_backend_url = os.getenv('REDIS_BACKEND_URL', 'redis://localhost:6379/0')

celery_app_instance = Celery(
    'fastapi_celery_tasks',
    broker=redis_broker_url,
    backend=redis_backend_url
)

celery_app_instance.autodiscover_tasks(['app.tasks'])


celery_app_instance.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'app.tasks.add',
        'schedule': 30.0,
        'args': (16, 16),
    },
    'log-current-time-daily': {
        'task': 'app.tasks.log_current_time',
        'schedule': crontab(hour=7, minute=30, day_of_week=1)
    },
}

celery_app_instance.conf.update(
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Europe/Kyiv',
    enable_utc=True,
)
