from django.db import models
from django.conf import settings
from apps.teams.models import Team

class Notification(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.team.name})"
