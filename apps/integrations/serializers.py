from rest_framework import serializers
from .models import GoogleCalendarToken

class GoogleTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleCalendarToken
        fields = ['id', 'access_token', 'refresh_token', 'token_expiry']
        read_only_fields = ['id', 'token_expiry']
