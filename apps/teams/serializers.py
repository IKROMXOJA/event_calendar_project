from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Team

User = get_user_model()

class TeamSerializer(serializers.ModelSerializer):
    admin = serializers.ReadOnlyField(source='admin.username')
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'admin', 'members', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        members = validated_data.pop('members', [])
        team = Team.objects.create(admin=self.context['request'].user, **validated_data)
        team.members.set(members)
        team.save()
        return team
