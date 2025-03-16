# Authors: Will Cooke and Tim Mishakov

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from leaderboard.models import Leaderboard

class HomeViewTest(TestCase):
    
    def setUp(self):
        """Set up a test client and test users with leaderboard entries."""
        self.client = Client()
        # Create the primary user for authentication.
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a leaderboard entry for the primary user with a score of 100.
        Leaderboard.objects.create(user=self.user, score=100)
        
        # Create additional users and their leaderboard entries.
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.user3 = User.objects.create_user(username='user3', password='password123')
        Leaderboard.objects.create(user=self.user2, score=200)
        Leaderboard.objects.create(user=self.user3, score=150)
    
    def test_home_renders_for_authenticated_user(self):
        """Test if authenticated users can access the home page."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')

    def test_home_context_contains_user_data(self):
        """Test if the home page context contains user data."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'testuser')
        self.assertContains(response, '100')
    
    def test_leaderboard_section_renders_correctly(self):
        """Test that the leaderboard section renders with correct ordering and progress."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        content = response.content.decode('utf-8')
        # Check that the leaderboard container and header are present.
        self.assertIn('<div class="leaderboard-container">', content)
        self.assertIn('<h4 class="text-center">Leaderboard</h4>', content)
        
        # The aggregation in the view orders entries as:
        #   user2: score=200 => progress: 200/200*100 = 100%
        #   user3: score=150 => progress: 150/200*100 = 75%
        #   testuser: score=100 => progress: 100/200*100 = 50%
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
        """Test that the empty leaderboard message is shown when no leaderboard data exists."""
        # Remove all leaderboard entries.
        Leaderboard.objects.all().delete()
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No leaderboard data available.')
