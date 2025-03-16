from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class ArticlesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.articles_url = reverse('articles')
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_articles_page_loads(self):
        """Test that the articles page loads successfully."""
        # Log in the user first
        self.client.login(username='testuser', password='testpassword')
        # Now access the articles page
        response = self.client.get(self.articles_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Educational Articles")

