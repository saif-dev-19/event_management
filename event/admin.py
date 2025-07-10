from django.contrib import admin
from event.models import Event,Category,Participant
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Participant)

