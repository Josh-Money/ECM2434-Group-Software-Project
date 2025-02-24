from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import Sum
from leaderboard.models import Leaderboard
from profiles.models import Profile

User = get_user_model()

class ProfileAppTests(TestCase):
    def setUp(self):
        # Create a test user and log them in.
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.force_login(self.user)
    
    def test_profile_signal_creates_profile(self):
        """
        Test that a Profile is automatically created when a new User is created.
        """
        # The signal should have created a profile for self.user.
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, Profile)
    
    def test_profile_view_status_and_template(self):
        """
        Test that the profile view returns a 200 status code and uses the correct template.
        """
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
    
    def test_profile_view_context(self):
        """
        Test that the profile view context contains the correct total_score and rank.
        """
        # Create two leaderboard entries for our test user.
        Leaderboard.objects.create(user=self.user, activity_type='main', score=10)
        Leaderboard.objects.create(user=self.user, activity_type='qr_scan', score=20)
        # Total score for testuser should be 30.
        
        # Create another user with a higher score to affect the ranking.
        other_user = User.objects.create_user(username='otheruser', password='testpassword')
        # Force login as other_user temporarily to create their scores.
        self.client.force_login(other_user)
        Leaderboard.objects.create(user=other_user, activity_type='main', score=50)
        # Log back in with testuser.
        self.client.force_login(self.user)
        
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Verify that total_score is correctly calculated.
        self.assertEqual(response.context['total_score'], 30)
        
        # Since otheruser has 50 points and testuser has 30, testuser should be rank 2.
        self.assertEqual(response.context['rank'], 2)
