# Author: Josh Money

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.db.models import Sum
from leaderboard.utils import update_leaderboard
from leaderboard.models import Leaderboard
from django.urls import reverse
import json

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
        self.client = Client()
        self.leaderboard_url = reverse('leaderboard')
        
        # Create test users
        self.user1 = User.objects.create_user(
            username='user1@exeter.ac.uk',
            email='user1@exeter.ac.uk',
            password='password123'
        )
        
        self.user2 = User.objects.create_user(
            username='user2@exeter.ac.uk',
            email='user2@exeter.ac.uk',
            password='password123'
        )
        
        self.user3 = User.objects.create_user(
            username='user3@exeter.ac.uk',
            email='user3@exeter.ac.uk',
            password='password123'
        )
        
        # Create leaderboard entries
        update_leaderboard(self.user1, 'main', points=100)
        update_leaderboard(self.user2, 'main', points=200)
        update_leaderboard(self.user3, 'main', points=150)

    def test_new_user_has_leaderboard_entry(self):
        """Test that a new user automatically gets a leaderboard entry."""
        new_user = User.objects.create_user(
            username='newuser@exeter.ac.uk',
            email='newuser@exeter.ac.uk',
            password='password123'
        )
        
        # Check if leaderboard entry was created
        entry = Leaderboard.objects.filter(user=new_user).exists()
        self.assertTrue(entry)

    def test_update_same_activity(self):
        """Test updating points for the same activity."""
        # Initial points
        initial_points = Leaderboard.objects.get(user=self.user1, activity_type='main').score
        
        # Update points for an activity
        update_leaderboard(self.user1, 'quiz', points=10)
        
        # Check if points were updated
        total_points = Leaderboard.objects.filter(user=self.user1).aggregate(total=Sum('score'))['total']
        self.assertEqual(total_points, initial_points + 10)
        
        # Update points for the same activity again
        update_leaderboard(self.user1, 'quiz', points=5)
        
        # Check if points were updated correctly
        quiz_points = Leaderboard.objects.get(user=self.user1, activity_type='quiz').score
        self.assertEqual(quiz_points, 15)

    def test_user_recieves_points_overall(self):
        """Test that a user receives points in the overall category."""
        # Initial points
        initial_points = Leaderboard.objects.filter(user=self.user1).aggregate(total=Sum('score'))['total']
        
        # Update points for an activity
        update_leaderboard(self.user1, 'travel', points=20)
        
        # Check if overall points were updated
        new_total = Leaderboard.objects.filter(user=self.user1).aggregate(total=Sum('score'))['total']
        self.assertEqual(new_total, initial_points + 20)

    def test_overall_leaderboard_ordering(self):
        """Test that the overall leaderboard is ordered correctly."""
        # Get all leaderboard entries ordered by score
        leaderboard_data = (
            Leaderboard.objects.filter(activity_type='main')
            .order_by('-score')
        )
        
        # Check if the ordering is correct
        self.assertEqual(leaderboard_data[0].user, self.user2)  # 200 points
        self.assertEqual(leaderboard_data[1].user, self.user3)  # 150 points
        self.assertEqual(leaderboard_data[2].user, self.user1)  # 100 points
        
    def test_leaderboard_page_loads(self):
        """Test that the leaderboard page loads successfully."""
        # Login the user
        self.client.login(username='user1@exeter.ac.uk', password='password123')
        response = self.client.get(self.leaderboard_url)
        self.assertEqual(response.status_code, 200)
        
    def test_leaderboard_contains_users(self):
        """Test that the leaderboard page contains the test users."""
        # Login the user
        self.client.login(username='user1@exeter.ac.uk', password='password123')
        response = self.client.get(self.leaderboard_url)
        self.assertContains(response, 'user1@exeter.ac.uk')
        self.assertContains(response, 'user2@exeter.ac.uk')
        self.assertContains(response, 'user3@exeter.ac.uk')
        
    def test_leaderboard_requires_login(self):
        """Test that the leaderboard page requires login."""
        response = self.client.get(self.leaderboard_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, '/')


