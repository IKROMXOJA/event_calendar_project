from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from .tasks import send_notification_task

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(team__members=user) | Notification.objects.filter(team__admin=user)

    def perform_create(self, serializer):
        notif = serializer.save(created_by=self.request.user)
        if notif.scheduled_at is None:
            send_notification_task.delay(notif.id)

    @action(detail=True, methods=['post'], url_path='send-now')
    def send_now(self, request, pk=None):
        notif = self.get_object()
        if notif.team.admin != request.user:
            return Response({"detail": "Ruxsat yo‘q"}, status=status.HTTP_403_FORBIDDEN)
        send_notification_task.delay(notif.id)
        return Response({"detail": "Xabar yuborildi."})
