# Author: Josh Money

from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import Sum
from leaderboard.utils import update_leaderboard
from leaderboard.models import Leaderboard

# Create your tests here.

class LeaderboardSignalTests(TestCase):
    def test_new_user_has_leaderboard_entry(self):
        """
        When a new user is created, the signal should automatically create a leaderboard
        entry (for the default activity, e.g. 'main'). The new entry should have 0 points.
        """
        user = User.objects.create_user(username='testuser', password='password123')

        entries = Leaderboard.objects.filter(user=user)
        self.assertTrue(entries.exists(), "No leaderbord entry was create for the new user")
        for entry in entries:
            self.assertEqual(entry.score, 0, "New leaderboard entry should have 0 points.")

class LeaderboardTests(TestCase):

    def setUp(self):
        """
        Set up a test user to test points gained in leaderboard. 
        """
        self.user = User.objects.create_user(username='testuser', password='password123')
    
    def test_update_same_activity(self):
        """
        Test that multiple updates to same activity increments the score
        rather than creating new records.
        """
        update_leaderboard(self.user, 'quiz', points=10)
        update_leaderboard(self.user, 'quiz', points=20)
        record = Leaderboard.objects.get(user=self.user, activity_type='quiz')
        self.assertEqual(record.score, 30)
    
    def test_user_recieves_points_overall(self):
        """
        Test that when a user receives points for multiple tasks,
        the overall aggregated score is calculated correctly.
        """
        update_leaderboard(self.user, 'quiz', points=10)
        update_leaderboard(self.user, 'qr_scan', points=20)
        update_leaderboard(self.user, 'travel', points=5)
        overall = Leaderboard.objects.filter(user=self.user).aggregate(total=Sum('score'))['total']
        self.assertEqual(overall, 35)

    def test_overall_leaderboard_ordering(self):
        """
        Test that the overall leaderboard correctly orders user based on their aggregate score.
        """

        user2 = User.objects.create_user(username='user2', password='password123')
        update_leaderboard(self.user, 'quiz', points=10)
        update_leaderboard(user2, 'quiz', points=20)

        leaderboard_data = (
            Leaderboard.objects.values('user__username')
            .annotate(total_score=Sum('score'))
            .order_by('-total_score')
        )

        self.assertEqual(leaderboard_data[0]['user__username'], 'user2')
        self.assertEqual(leaderboard_data[0]['total_score'], 20)

        self.assertEqual(leaderboard_data[1]['user__username'], 'testuser')
        self.assertEqual(leaderboard_data[1]['total_score'], 10)


