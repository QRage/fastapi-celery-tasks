from pydantic import BaseModel

from fastapi import FastAPI
from celery import chain, group

from app.celery_app import celery_app_instance as celery_app
from app.tasks import (
    send_welcome_email,
    process_large_data,
    task1,
    task2,
    task3,
    long_running_task,
    process_item
)


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




@app.post('/chain-example', response_model=TaskResponse)
async def run_chain():
    result = chain(task1.s(10), task2.s(), task3.s()).delay()
    return TaskResponse(task_id=result.id, status='QUEUED', message='Chain started')


@app.post('/group-example', response_model=TaskResponse)
async def run_group():
    item_ids = [1, 2, 3, 4, 5]
    result = group(process_item.s(item_id) for item_id in item_ids).delay()
    return TaskResponse(task_id=result.id, status='QUEUED', message='Group started')


@app.post('/run-long-task', response_model=TaskResponse)
async def run_long_task():
    task = long_running_task.delay(10)
    return TaskResponse(task_id=task.id, status='QUEUED', message='Long running task started')


@app.get('/task-status/{task_id}')
async def get_task_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
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
