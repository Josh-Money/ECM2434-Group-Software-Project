from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class ChallengesTests(TestCase):
    """Tests for the challenges app functionality."""
    
    def setUp(self):
        """Set up test data and client."""
        self.client = Client()
        self.challenges_url = reverse('challenges')
        
        # Create a test user
        self.test_user = User.objects.create_user(
            username='testuser@exeter.ac.uk',
            email='testuser@exeter.ac.uk',
            password='testpassword123'
        )
    
    def test_challenges_page_requires_login(self):
        """Test that the challenges page requires login."""
        response = self.client.get(self.challenges_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, '/')
    
    def test_challenges_page_loads(self):
        """Test that the challenges page loads successfully when logged in."""
        # Login the user
        self.client.login(username='testuser@exeter.ac.uk', password='testpassword123')
        response = self.client.get(self.challenges_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'challenges/challenges.html')
    
    def test_challenges_page_content(self):
        """Test that the challenges page contains expected content when logged in."""
        # Login the user
        self.client.login(username='testuser@exeter.ac.uk', password='testpassword123')
        response = self.client.get(self.challenges_url)
        self.assertContains(response, 'Challenges')
    
    def test_challenges_authenticated_user(self):
        """Test that authenticated users can access the challenges page."""
        self.client.login(username='testuser@exeter.ac.uk', password='testpassword123')
        response = self.client.get(self.challenges_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'challenges/challenges.html')
