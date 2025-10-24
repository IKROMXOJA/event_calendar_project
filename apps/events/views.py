from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime
from .models import Event
from .serializers import EventSerializer

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['patch'], url_path='drag-update')
    def drag_update(self, request, pk=None):
        event = self.get_object()
        start = request.data.get('start_date')
        end = request.data.get('end_date')

        if start:
            event.start_date = parse_datetime(start)
        if end:
            event.end_date = parse_datetime(end)
        event.save()
        return Response(EventSerializer(event).data, status=status.HTTP_200_OK)
