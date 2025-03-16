# Authors: Will Cooke and Tim Mishakov

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from leaderboard.models import Leaderboard

class HomeViewTest(TestCase):
    
    def setUp(self):
        """Set up stuff for testing."""
        self.client = Client()
        # Make a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Give the user some points
        Leaderboard.objects.create(user=self.user, score=100)
        
        # Make some more users with different scores
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.user3 = User.objects.create_user(username='user3', password='password123')
        Leaderboard.objects.create(user=self.user2, score=200)
        Leaderboard.objects.create(user=self.user3, score=150)
    
    def test_home_renders_for_authenticated_user(self):
        """Check if logged in users can see the home page."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')

    def test_home_redirects_unauthenticated_user(self):
        """Check if logged out users get redirected from home page."""
        response = self.client.get(reverse('home'))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        # Check if it redirects to login
        self.assertRedirects(response, '/')

    def test_home_context_contains_user_data(self):
        """Check if the page shows the user's name and points."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'testuser')
        self.assertContains(response, '100')
    
    def test_leaderboard_section_renders_correctly(self):
        """Check if the leaderboard shows up right with correct scores and progress bars."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        content = response.content.decode('utf-8')
        # Check for leaderboard container
        self.assertIn('<div class="leaderboard-container">', content)
        self.assertIn('<h4 class="subtitle">Leaderboard</h4>', content)
        
        # The scores should be ordered like:
        #   user2: 200 points = 100% progress
        #   user3: 150 points = 75% progress
        #   testuser: 100 points = 50% progress
        self.assertIn('user2', content)
        self.assertIn('200', content)
        self.assertIn('width: 100%;', content)
        
        self.assertIn('user3', content)
        self.assertIn('150', content)
        self.assertIn('width: 75%;', content)
        
        self.assertIn('testuser', content)
        self.assertIn('100', content)
        self.assertIn('width: 50%;', content)
        
    
    def test_leaderboard_empty(self):
        """Check if we show a message when there's no leaderboard data."""
        # Delete all leaderboard entries
        Leaderboard.objects.all().delete()
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No leaderboard data available.')
