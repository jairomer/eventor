from django.db import models
from django.contrib.auth.models import User

# An Event is always related to a user
class EventModel(models.Model):
    owner = models.ForeignKey('auth.User', related_name='owner', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    nearestStation = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title}: {self.subtitle} on {self.date} belonging to {self.owner}"
