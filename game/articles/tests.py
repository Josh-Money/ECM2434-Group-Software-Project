from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article, Quiz, Question

class ArticlesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.articles_url = reverse('articles:articles')
        self.question_answer_url = reverse('articles:get_question_answer', args=[1])
        
        # Create a test user
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Create test article with quiz
        self.article = Article.objects.create(
            title='Test Article',
            content='Test content'
        )
        
        self.quiz = Quiz.objects.create(
            article=self.article,
            title='Test Quiz',
            points_per_question=10
        )
        
        self.question = Question.objects.create(
            quiz=self.quiz,
            text='Test question',
            correct_answer='true',
            order=1
        )

    def test_articles_page_requires_login(self):
        """Test that the articles page requires login."""
        response = self.client.get(self.articles_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, '/')

    def test_articles_page_loads(self):
        """Test that the articles page loads successfully when logged in."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.articles_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/articles.html')
        self.assertContains(response, "Educational Articles")

    def test_article_with_quiz_display(self):
        """Test that articles with quizzes display correctly."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.articles_url)
        self.assertContains(response, self.article.title)
        self.assertContains(response, self.quiz.title)
        self.assertContains(response, self.question.text)

    def test_get_question_answer(self):
        """Test the API endpoint for getting question answers."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.question_answer_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['correct_answer'], 'true')

    def test_quiz_submission(self):
        """Test submitting quiz answers and points calculation."""
        self.client.login(username='testuser', password='testpassword123')
        
        # Submit quiz with correct answers
        response = self.client.post(self.articles_url, {
            'quiz_id': self.quiz.id,
            'correct_answers': 1  # One correct answer
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['points_earned'], 10)  # 10 points per question
        self.assertEqual(data['activity'], 'quiz')
        self.assertTrue(data['success'])

    def test_article_with_external_url(self):
        external_article = Article.objects.create(
            title='External Article',
            url='https://example.com/article'
        )
        
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.articles_url)
        self.assertContains(response, external_article.title)
        self.assertContains(response, external_article.url)

