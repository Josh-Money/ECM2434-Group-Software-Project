from django.db import models
<<<<<<< Updated upstream
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_profile.jpg', upload_to='profile_pics')
=======
from django.contrib.auth import get_user_model
from django.db.models import F, Window
from django.db.models.functions import Rank
from django.utils.timezone import localdate
from datetime import timedelta

User = get_user_model()

class Profile(models.Model):
    image = models.ImageField(default='images/profile_pics/default_profile.jpg', upload_to='profile_pics', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
>>>>>>> Stashed changes
    points = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'
