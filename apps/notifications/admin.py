from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'team', 'created_by', 'scheduled_at', 'is_sent')
    list_filter = ('is_sent', 'team')
    search_fields = ('title', 'message', 'team__name')
