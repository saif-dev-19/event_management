from django.contrib import admin
from django.urls import path,include
from debug_toolbar.toolbar import debug_toolbar_urls
from event.views import home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("event.urls"))
]+ debug_toolbar_urls()
