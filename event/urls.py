from event.views import show_event,create_event,create_category,create_participant,event_dashboard,update_event,home_page,participant_page,delete_event
from django.urls import path


urlpatterns = [
    path('show-event/',show_event),
    path("event-dashboard/",event_dashboard, name="event-dashboard"),
    path("create-event/",create_event , name="create-event"),
    path("create-category/",create_category, name="create-category"),
    path("create-participant/",create_participant, name="create-participant"),
    path("update-event/<int:id>/",update_event,name="update-event"),
    path("delete-event/<int:id>/",delete_event,name="delete-event"),
    path("home-page/",home_page,name="home-page"),
    path("participant-page/",participant_page,name="participant-page"),
    path('', home_page, name='home-page'),
]
