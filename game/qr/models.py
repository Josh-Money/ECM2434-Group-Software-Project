from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class QRScan(models.Model):
    """
    Model to track QR code scans with daily limitations
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scan_date = models.DateField(default=timezone.now)
    qr_code = models.CharField(max_length=100)
    points_earned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'scan_date', 'qr_code']

    def __str__(self):
        return f"{self.user.username} - {self.scan_date} - {self.points_earned} points"
