from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    team_name = serializers.ReadOnlyField(source='team.name')

    class Meta:
        model = Notification
        fields = ['id', 'team', 'team_name', 'title', 'message', 'created_by', 'scheduled_at', 'sent_at', 'is_sent']
        read_only_fields = ['id', 'created_by', 'sent_at', 'is_sent']
