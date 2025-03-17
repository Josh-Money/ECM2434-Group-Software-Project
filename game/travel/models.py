# Author Tim Mishakov
from django.db import models
from django.contrib.auth.models import User

class CampusTravel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    travel_method = models.CharField(max_length=50)
    points = models.PositiveIntegerField(default=0)
    lat = models.FloatField(null=True, blank=True)  
    lon = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} on {self.date} - {self.travel_method} ({self.points} pts)"
