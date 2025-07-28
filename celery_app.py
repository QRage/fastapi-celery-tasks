import os
from celery import Celery
import time


redis_broker_url = os.getenv('REDIS_BROKER_URL', 'redis://localhost:6379/0')
redis_backend_url = os.getenv('REDIS_BACKEND_URL', 'redis://localhost:6379/0')

app = Celery(
    'fastapi_celery_tasks',
    broker=redis_broker_url,
    backend=redis_backend_url
)

app.conf.update(
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Europe/Kyiv',
    enable_utc=True,
)

@app.task(name="send_welcome_email")
def send_welcome_email(user_email: str):
    """
    Celery task to simulate sending a welcome email.
    This task will take some time to execute.

    :param user_email: The email address of the user to send the welcome email to.
    :type user_email: str
    :return: A message indicating the email was sent.
    :rtype: str
    """
    print(f"--- Sending welcome email to {user_email} ---")
    time.sleep(10)
    print(f"--- Welcome email sent to {user_email}! ---")
    return f"Welcome email sent successfully to {user_email}"
