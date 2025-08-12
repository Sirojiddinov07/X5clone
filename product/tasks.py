import requests
from celery import shared_task


@shared_task
def generate_replenishment_reports():
    API_URL = "http://127.0.0.1:8000/replenishment-data/"

    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return f"Ma'lumotlar muvaffaqiyatli olingan. Javob: {response.json()}"
    except requests.exceptions.RequestException as e:
        return f"Xato yuz berdi: {str(e)}"