from celery import shared_task
import requests

@shared_task
def send_telegram_message(chat_id, message):
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': message}
    requests.post(url, data=payload)