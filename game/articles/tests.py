from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class ArticlesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.articles_url = reverse('articles:articles')  
        self.quiz_submission_url = reverse('articles:articles') 
        # Create a test user
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )

    def test_articles_page_loads(self):
        """Test that the articles page loads successfully."""
        # Login the test user
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.articles_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Educational Articles")
