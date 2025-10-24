from django.urls import path
from .views import GoogleAuthCallbackView, GoogleDisconnectView

urlpatterns = [
    path('callback/', GoogleAuthCallbackView.as_view(), name='google_callback'),
    path('disconnect/', GoogleDisconnectView.as_view(), name='google_disconnect'),
]
