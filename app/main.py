from pydantic import BaseModel

from fastapi import FastAPI

from app.celery_app import celery_app_instance
from app.tasks import send_welcome_email, process_large_data


app = FastAPI(
    title='FastAPI Celery Async Tasks',
    description='A simple FastAPI app, for asnyc task process with Celery and Redis.',
    version='1.0.0'
)


class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str = 'Task successfully queued.'


class EmailRequest(BaseModel):
    email: str


class DataProcessRequest(BaseModel):
    data_id: int


@app.get('/')
async def root():
    return {'message': 'Welcome to the FastAPI Celery Demo! Visit /docs for more info.'}


@app.post('/send-async-email', response_model=TaskResponse)
def trigger_send_email_task(request: EmailRequest):
    task = send_welcome_email.delay(request.email)
    return TaskResponse(task_id=task.id, status='QUEUED')


@app.post('/process-data', response_model=TaskResponse)
def trigger_process_data_task(request: DataProcessRequest):
    task = process_large_data.delay(request.data_id)
    return TaskResponse(task_id=task.id, status='QUEUED')


@app.get('/task-status/{task_id}')
async def get_task_status(task_id: str):
    task = celery_app_instance.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'status': task.state,
            'result': 'Task is pending or has not started yet.'
        }
    elif task.state == 'FAILURE':
        response = {
            'status': task.state,
            'result:': str(task.result),
            'traceback': task.traceback
        }
    else:
        response = {
            'status': task.state,
            'result': task.result
        }
    return response
