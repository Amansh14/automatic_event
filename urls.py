

from django.urls import path
from . import views

urlpatterns = [
    path('send-event-emails/', views.send_event_emails_view, name='send-event-emails'),
    # Add other URLs if needed
]
