from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class ContactTests(TestCase):
    """Tests for the contact app functionality."""
    
    def setUp(self):
        """Set up test data and client."""
        self.client = Client()
        self.contact_url = reverse('contact')
        
        # Create a test user
        self.test_user = User.objects.create_user(
            username='testuser@exeter.ac.uk',
            email='testuser@exeter.ac.uk',
            password='testpassword123'
        )
    
    def test_contact_page_requires_login(self):
        """Test that the contact page requires login."""
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, '/')
    
    def test_contact_page_loads(self):
        """Test that the contact page loads successfully when logged in."""
        # Login the user
        self.client.login(username='testuser@exeter.ac.uk', password='testpassword123')
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')
    
    def test_contact_page_content(self):
        """Test that the contact page contains expected content when logged in."""
        # Login the user
        self.client.login(username='testuser@exeter.ac.uk', password='testpassword123')
        response = self.client.get(self.contact_url)
        self.assertContains(response, 'Contact')
    
    def test_contact_authenticated_user(self):
        """Test that authenticated users can access the contact page."""
        self.client.login(username='testuser@exeter.ac.uk', password='testpassword123')
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')
