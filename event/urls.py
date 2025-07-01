from event.views import show_event,dashboard
from django.urls import path


urlpatterns = [
    path('show-event/',show_event),
    path("dashboard/",dashboard)
]
