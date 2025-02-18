from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from leaderboard.models import Leaderboard

def create_leaderboard_entry(sender, instance, created, **kwargs):
    if created:
        Leaderboard.objects.create(user=instance)