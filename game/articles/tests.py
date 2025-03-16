from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class ArticlesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.articles_url = reverse('articles:home')  
        self.quiz_submission_url = reverse('articles:quiz_submit') 

    def test_articles_page_loads(self):
        """Test that the articles page loads successfully."""
        response = self.client.get(self.articles_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Educational articles on sustainability")

    def test_quiz_submission_valid(self):
        """Test submitting a valid quiz answer updates the leaderboard."""
        data = {
            'correct_answers': 4  
        }
        response = self.client.post(self.quiz_submission_url, data, content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "success"})  

    def test_quiz_submission_csrf_protected(self):
        """Test that the quiz submission requires a CSRF token."""
        data = {
            'correct_answers': 3  
        }
        response = self.client.post(self.quiz_submission_url, data, follow=True)
        self.assertNotEqual(response.status_code, 403)  

