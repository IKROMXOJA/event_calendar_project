from rest_framework import status, views, permissions
from rest_framework.response import Response
from django.conf import settings
from django.utils import timezone
import requests, datetime
from .models import GoogleCalendarToken
from .serializers import GoogleTokenSerializer

class GoogleAuthCallbackView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        code = request.GET.get('code')
        if not code:
            return Response({"error": "code yo‘q"}, status=400)

        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        r = requests.post("https://oauth2.googleapis.com/token", data=data)
        if r.status_code != 200:
            return Response({"error": "Google token olishda xato"}, status=400)

        res = r.json()
        token_obj, _ = GoogleCalendarToken.objects.update_or_create(
            user=request.user,
            defaults={
                "access_token": res['access_token'],
                "refresh_token": res['refresh_token'],
                "token_expiry": timezone.now() + datetime.timedelta(seconds=res['expires_in'])
            }
        )
        return Response(GoogleTokenSerializer(token_obj).data)

class GoogleDisconnectView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        GoogleCalendarToken.objects.filter(user=request.user).delete()
        return Response({"detail": "Google Calendar uzildi"}, status=204)
