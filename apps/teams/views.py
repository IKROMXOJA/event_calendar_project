from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Team
from .serializers import TeamSerializer

class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Team.objects.filter(members=user) | Team.objects.filter(admin=user)

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)

    @action(detail=True, methods=['post'], url_path='add-member')
    def add_member(self, request, pk=None):
        team = self.get_object()
        if team.admin != request.user:
            return Response({"detail": "Sizda huquq yo‘q."}, status=status.HTTP_403_FORBIDDEN)
        user_id = request.data.get('user_id')
        team.members.add(user_id)
        return Response({"detail": "Foydalanuvchi qo‘shildi."})

    @action(detail=True, methods=['post'], url_path='remove-member')
    def remove_member(self, request, pk=None):
        team = self.get_object()
        if team.admin != request.user:
            return Response({"detail": "Sizda huquq yo‘q."}, status=status.HTTP_403_FORBIDDEN)
        user_id = request.data.get('user_id')
        team.members.remove(user_id)
        return Response({"detail": "Foydalanuvchi o‘chirildi."})
