import time
import requests
from datetime import datetime

from app.celery_app import celery_app_instance as app


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


@app.task
def add(x: int, y: int):
    result = x + y
    return result


@app.task
def log_current_time():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f'Current time logged: {current_time}'


@app.task
def task1(value: int):
    time.sleep(2)
    return value + 1


@app.task
def task2(value: int):
    time.sleep(2)
    return value * 2


@app.task
def task3(value: int):
    time.sleep(2)
    return value - 5


@app.task
def long_running_task(duration: int):
    time.sleep(duration)
    return f'Task completed in {duration} seconds.'


@app.task
def process_item(item_id: int):
    time.sleep(1)
    return f'Item {item_id} processed'


@app.task
def get_current_weather(city: str, api_key: str):
    """
    Simulates fetching current weather data for a given city from OpenWeatherMap.
    """
    print(f"Fetching weather for {city}...")
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        
        result_message = f"Weather in {city}: {description}, {temperature}°C."
        print(result_message)
        
        return result_message
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch weather data: {e}")
        return f"Error: Failed to fetch weather data for {city}."