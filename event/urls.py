from event.views import rspv_event, show_event,create_event,create_category,organizer_dashboard, dashboard,create_participant,user_dashboard,update_event,home_page,participant_page,delete_event,event_detials
from django.urls import path
from core.views import no_permission

urlpatterns = [
    path('show-event/',show_event),
    path("event-dashboard/",user_dashboard, name="event-dashboard"),
    path("create-event/",create_event , name="create-event"),
    path("create-category/",create_category, name="create-category"),
    path("create-participant/",create_participant, name="create-participant"),
    path("update-event/<int:id>/",update_event,name="update-event"),
    path("delete-event/<int:id>/",delete_event,name="delete-event"),
    path("home-page/",home_page,name="home-page"),
    path("participant-page/",participant_page,name="participant-page"),
    path("no-permission/",no_permission,name="no-permission"),
    path("event/<int:event_id>/deitals/",event_detials,name="event-detials"),
    path("organizer-dashboard/",organizer_dashboard,name="organizer-dashboard"),
    path('dashboard/',dashboard,name='dashboard'),
    path('event/<int:event_id>/rspv-event/',rspv_event,name="rspv-event")
]
