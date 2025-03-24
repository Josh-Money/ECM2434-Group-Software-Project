from django.db import models
from django.utils import timezone

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    description = models.TextField()
    subscription = models.CharField(max_length=255, blank=True, null=True, 
                                  help_text="Information on how to subscribe/register for the event")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date', 'time']
    
    def __str__(self):
        return self.title
    
    @property
    def is_past(self):
        """Check if the event has already occurred"""
        event_datetime = timezone.make_aware(
            timezone.datetime.combine(self.date, self.time)
        )
        return event_datetime < timezone.now()
