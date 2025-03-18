from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    url = models.URLField(blank=True, null=True, help_text="Optional external URL to article content")
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Quiz(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField(max_length=255)
    points_per_question = models.PositiveIntegerField(default=10, help_text="Points awarded per correct answer")
    
    def __str__(self):
        return f"Quiz for {self.article.title}"


class Question(models.Model):
    BOOL_CHOICES = (
        ('true', 'True'),
        ('false', 'False'),
    )
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    correct_answer = models.CharField(max_length=10, choices=BOOL_CHOICES)
    order = models.PositiveIntegerField(default=0, help_text="Order of question in the quiz")
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Question {self.order} for {self.quiz}"
