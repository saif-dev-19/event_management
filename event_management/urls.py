from event.views import home
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',home),
    path('event/',include("event.urls"))
]
