
from django.db import models
<<<<<<< Updated upstream
from django.contrib.auth.models import User

class Profile(models.Model):
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
    longest_streak = models.IntegerField(default=0)

    def add_points(self, amount):
        """Add points to the user and update rankings."""
        self.points += amount
        self.save()
        self.update_ranks()

        # Updating log
        UserPointLog.objects.create(user=self.user, points_added=amount)

    def get_points(self):
        """Return the user's current points."""
        return self.points

    def get_rank(self):
        # Compute the rank for all profiles
        ranked_profiles = list(Profile.objects.annotate(
            rank=Window(expression=Rank(), order_by=F('points').desc())
        ))
        # Find the rank for the current profile in Python
        for profile in ranked_profiles:
            if profile.user == self.user:
                return profile.rank
        return None
    @classmethod
    def update_ranks(cls):
        """Recalculate and update ranks for all users."""
        ranked_users = cls.objects.annotate(rank=Window(expression=Rank(), order_by=F('points').desc()))
        for profile in ranked_users:
            profile.rank = profile.rank  # Store the rank in the database if needed
            profile.save()

    def get_streak(self):
        """Calculate the current streak based on logs and update longest streak if necessary."""
        logs = UserPointLog.objects.filter(user=self.user).order_by('-timestamp')
        if not logs:
            return 0  # No logs, no streak

        today = localdate()
        streak = 0
        expected_date = today

        for log in logs:
            log_date = log.timestamp.date()
            if log_date == expected_date:
                streak += 1
                expected_date -= timedelta(days=1)  # Move to the previous day
            elif log_date < expected_date:
                break  # Streak is broken

        # Update longest streak if needed
        if streak > self.longest_streak:
            self.longest_streak = streak
            self.save()

        return streak

class UserPointLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="point_logs")
    points_added = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)  # When points were added

    def __str__(self):
        return f"{self.user.username} gained {self.points_added} points on {self.timestamp}"
