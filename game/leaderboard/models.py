#Author: Joshua Money
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Leaderboard(models.Model):

    ACTIVITY_CHOICES = [
        ('main', 'Main'),
        ('qr_scan', 'QR Scan'),
        ('quiz', 'Article Quiz'),
        ('travel', 'Travel Log'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=10, choices=ACTIVITY_CHOICES)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.score}"
