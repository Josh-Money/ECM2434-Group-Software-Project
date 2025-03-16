from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import Sum
from leaderboard.models import Leaderboard
from profiles.models import Profile

User = get_user_model()

class ProfileAppTests(TestCase):
    def setUp(self):
        # Make a test user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.force_login(self.user)
    
    def test_profile_signal_creates_profile(self):
        """
        Check if a Profile gets made automatically when a new User is created.
        """
        # Should have created a profile for our user
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, Profile)
    
    def test_profile_default_image(self):
        """
        Check if new profiles get the default image.
        """
        # New profiles should have the default image
        self.assertEqual(self.user.profile.image, 'default_profile.jpg')
        
    def test_profile_default_points(self):
        """
        Check if new profiles start with 0 points.
        """
        # New profiles should start with 0 points
        self.assertEqual(self.user.profile.points, 0)
    
    def test_profile_view_status_and_template(self):
        """
        Check if the profile page loads and uses the right template.
        """
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
    
    def test_profile_view_context(self):
        """
        Check if the profile page shows the right score and rank.
        """
        # Add some points for our test user
        Leaderboard.objects.create(user=self.user, activity_type='main', score=10)
        Leaderboard.objects.create(user=self.user, activity_type='qr_scan', score=20)
        # Total should be 30
        
        # Make another user with more points to test ranking
        other_user = User.objects.create_user(username='otheruser', password='testpassword')
        # Log in as other user to add their points
        self.client.force_login(other_user)
        Leaderboard.objects.create(user=other_user, activity_type='main', score=50)
        # Switch back to our main test user
        self.client.force_login(self.user)
        
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Check total score
        self.assertEqual(response.context['total_score'], 30)
        
        # Our user should be rank 2 (other user has more points)
        self.assertEqual(response.context['rank'], 2)
