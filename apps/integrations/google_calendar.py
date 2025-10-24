import datetime
import requests
from django.conf import settings
from django.utils import timezone
from .models import GoogleCalendarToken

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/primary/events"

def refresh_google_token(token_obj: GoogleCalendarToken):
    data = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "refresh_token": token_obj.refresh_token,
        "grant_type": "refresh_token",
    }
    r = requests.post(GOOGLE_TOKEN_URL, data=data)
    if r.status_code == 200:
        res = r.json()
        token_obj.access_token = res['access_token']
        token_obj.token_expiry = timezone.now() + datetime.timedelta(seconds=res['expires_in'])
        token_obj.save()
    else:
        raise Exception("Tokenni yangilab bo‘lmadi")

def get_auth_header(user):
    token = GoogleCalendarToken.objects.get(user=user)
    if timezone.now() >= token.token_expiry:
        refresh_google_token(token)
    return {"Authorization": f"Bearer {token.access_token}", "Content-Type": "application/json"}

def create_google_event(user, event):
    data = {
        "summary": event.title,
        "description": event.description,
        "start": {"dateTime": event.start_time.isoformat(), "timeZone": "Asia/Tashkent"},
        "end": {"dateTime": event.end_time.isoformat(), "timeZone": "Asia/Tashkent"}
    }
    r = requests.post(GOOGLE_EVENTS_URL, headers=get_auth_header(user), json=data)
    return r.json()

def update_google_event(user, google_event_id, event):
    data = {
        "summary": event.title,
        "description": event.description,
        "start": {"dateTime": event.start_time.isoformat(), "timeZone": "Asia/Tashkent"},
        "end": {"dateTime": event.end_time.isoformat(), "timeZone": "Asia/Tashkent"}
    }
    r = requests.patch(f"{GOOGLE_EVENTS_URL}/{google_event_id}", headers=get_auth_header(user), json=data)
    return r.json()

def delete_google_event(user, google_event_id):
    r = requests.delete(f"{GOOGLE_EVENTS_URL}/{google_event_id}", headers=get_auth_header(user))
    return r.status_code == 204
