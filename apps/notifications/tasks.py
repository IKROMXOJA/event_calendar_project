from celery import shared_task
from django.utils import timezone
from .models import Notification
from apps.users.models import User
from .utils import send_email_notification, send_telegram_message

@shared_task
def send_notification_task(notification_id):
    notification = Notification.objects.get(id=notification_id)
    members = notification.team.members.all()

    for member in members:
        if hasattr(member, 'telegram_id') and member.telegram_id:
            send_telegram_message(member.telegram_id, f"{notification.title}\n\n{notification.message}")
        if member.email:
            send_email_notification(member.email, notification.title, notification.message)

    notification.is_sent = True
    notification.sent_at = timezone.now()
    notification.save()

@shared_task
def schedule_notifications():
    now = timezone.now()
    notifications = Notification.objects.filter(is_sent=False, scheduled_at__lte=now)
    for notif in notifications:
        send_notification_task.delay(notif.id)
