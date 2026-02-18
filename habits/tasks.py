from celery import shared_task
import requests
import os
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_telegram_message(chat_id, message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        logger.info(f"Сообщение отправлено пользователю {chat_id}: {message}")
        return f"Сообщение отправлено: {message}"
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка отправки сообщения: {e}")
        return f"Ошибка отправки: {e}"


@shared_task
def test_task():
    return f"Задача выполнена:="
