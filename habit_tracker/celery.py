import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "habit_tracker.settings")
app = Celery("habit_tracker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send-daily-reminders": {
        "task": "habits.tasks.send_telegram_message",
        "schedule": crontab(hour=9, minute=0),  # Каждый день в 9:00
        "args": ("1301021131", "Напоминание: выполните свои привычки!"),
    },
}
