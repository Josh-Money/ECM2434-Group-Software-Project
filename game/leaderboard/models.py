#Author: Joshua Money
from django.db import models

# Create your models here.

class Score(models.Model):

    ACTIVITY_CHOICES = [
        ('qr_scan', 'QR Scan'),
        ('quiz', 'Article Quiz'),
        ('travel', 'Travel Log'),
    ]

    player_name = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=10, choices=ACTIVITY_CHOICES)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']

    def __str__(self):
        return f"{self.player_name} - {self.activity_type} - {self.score}"
