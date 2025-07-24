from event.views import rspv_event, show_event,create_category,organizer_dashboard, dashboard,user_dashboard,home_page,participant_page,event_detials,dashboard
from django.urls import path
from core.views import no_permission
from event.views import CreateEventView,UpdateEventView,DeleteEventView,CreateCategoryEvent

urlpatterns = [
    path('show-event/',show_event),
    path("event-dashboard/",user_dashboard, name="event-dashboard"),
    path("create-event/",CreateEventView.as_view() , name="create-event"),
    path("create-category/",create_category, name="create-category"),
    path("create-participant/",CreateCategoryEvent.as_view(), name="create-participant"),
    path("update-event/<int:id>/",UpdateEventView.as_view(),name="update-event"),
    path("delete-event/<int:id>/",DeleteEventView.as_view(),name="delete-event"),
    path("home-page/",home_page,name="home-page"),
    path("participant-page/",participant_page,name="participant-page"),
    path("no-permission/",no_permission,name="no-permission"),
    path("event/<int:event_id>/deitals/",event_detials,name="event-detials"),
    path("organizer-dashboard/",organizer_dashboard,name="organizer-dashboard"),
    path('dashboard/',dashboard,name='dashboard'),
    path('event/<int:event_id>/rspv-event/',rspv_event,name="rspv-event"),
    path("dashboard/",dashboard,name="dashboard")
]
