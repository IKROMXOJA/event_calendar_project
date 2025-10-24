import os
from celery import Celery
from celery.schedules import crontab

# Django settings modulini ko‘rsatish
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('event_calendar_project')

# Django settings'dagi CELERY sozlamalarini yuklash
app.config_from_object('django.conf:settings', namespace='CELERY')

# Barcha app'lardan tasks.py fayllarini avtomatik yuklash
app.autodiscover_tasks()

# Rejalashtirilgan vazifalar (periodic tasks)
app.conf.beat_schedule = {
    'send-event-reminders': {
        'task': 'notifications.tasks.send_event_reminders',
        'schedule': crontab(minute='*/5'),  # har 5 daqiqada
    },
}
