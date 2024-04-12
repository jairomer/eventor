from django.db import models

# An Event is always related to a user
class EventModel(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    nearestStation = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title}: {self.subtitle} on {self.date}" 
