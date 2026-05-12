from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=80)
    capacity = models.PositiveIntegerField(default=50, validators=[MinValueValidator(1)])
    asset = models.ImageField(upload_to='event_asset',blank=True, null=True)
    category = models.ForeignKey("Category",on_delete=models.CASCADE, default=1)
    rspv = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="rspv_events", blank= True)
    is_rpsv = models.BooleanField(default=False)

    @property
    def rsvp_count(self):
        return self.rspv.count()

    @property
    def seats_left(self):
        return max(self.capacity - self.rsvp_count, 0)

    @property
    def is_full(self):
        return self.rsvp_count >= self.capacity

    def __str__(self):
        return self.name


class Participant(models.Model):
    name = models.CharField(max_length=200,)
    email = models.EmailField(unique=True)
    event = models.ManyToManyField(Event,related_name="participants")
    

    def __str__(self):
        return self.name
    



