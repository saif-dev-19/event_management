from django.contrib import admin
from django.urls import path,include
from debug_toolbar.toolbar import debug_toolbar_urls
from event.views import home_page
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('event/',include("event.urls")),
    path('users/',include("users.urls")),
    path('',home_page,name="home")
]+ debug_toolbar_urls()



urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
