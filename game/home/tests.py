from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class HomeViewTest(TestCase):
    
    def setUp(self):
        """Set up a test client and a test user"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_home_redirects_if_not_authenticated(self):
        """Test if unauthenticated users are redirected to '/'"""
        response = self.client.get(reverse('home'))  # Ensure 'home' matches the URL name
        self.assertEqual(response.status_code, 302)  # Redirect expected
        self.assertRedirects(response, '/')  # Ensure it redirects to home page

    def test_home_renders_for_authenticated_user(self):
        """Test if authenticated users can access the home page"""
        self.client.login(username='testuser', password='testpassword')  # Log in user
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)  # Page should load successfully
        self.assertTemplateUsed(response, 'home/home.html')  # Ensure correct template is used

    def test_home_context_contains_user_data(self):
        """Test if the home page context contains user data"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'testuser')  # Ensure username is displayed
        self.assertContains(response, '100')  # Ensure points are displayed
