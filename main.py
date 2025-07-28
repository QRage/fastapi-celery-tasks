from fastapi import FastAPI, HTTPException, status
from typing import List, Dict, Any
from datetime import datetime
from contextlib import asynccontextmanager

from celery_app import app as celery_app, send_welcome_email


app = FastAPI(
    title="FastAPI Celery Async Tasks",
    description="A simple FastAPI app, for asnyc task process with Celery and Redis.",
    version="1.0.0"
)


@app.get("/", summary="API Root Greeting")
async def root():
    return {"message": "Welcome to the FastAPI Celery Demo! Visit /docs for more info."}


@app.post("/send-async-email", status_code=status.HTTP_202_ACCEPTED, summary="Trigger async email sending")
async def trigger_async_email(email: str = "test@example.com"):
    task = send_welcome_email.delay(email)
    return {"message": f"Email sending task initiated for {email}", "task_id": task.id}


@app.get("/task-status/{task_id}", summary="Get Celery task status")
async def get_celery_task_status(task_id: str):
    task_result = celery_app.AsyncResult(task_id)
    response_data = {
        "task_id": task_id,
        "status": task_result.status
    }
    if task_result.ready():
        response_data["result"] = task_result.get()
    elif task_result.state == 'FAILURE':
        response_data["error"] = str(task_result.info)
    return response_data