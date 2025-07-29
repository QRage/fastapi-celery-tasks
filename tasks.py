import time

from celery_app import celery_app_instance as app


@app.task(name='send_welcome_email')
def send_welcome_email(email: str):
    print(f'Sending welcome email to {email}...')
    time.sleep(10)
    print(f'Welcome email sent to {email}')
    return {"status": "Email sent", "recipient": email}


@app.task(name='process_large_data')
def process_large_data(data_id: int):
    print(f"Processing large data for ID: {data_id}...")
    for i in range(5):
        time.sleep(2)
        print(f'    Processing step {i+1} for data ID {data_id}')
    result = f'Data with ID {data_id} processed successfully.'
    print(result)
    return {"status": "Processed", "data_id": data_id, "result": result}
