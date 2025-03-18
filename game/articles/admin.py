from django.contrib import admin
from .models import Article, Quiz, Question

# Register your models here.
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 5

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'has_quiz')
    search_fields = ('title', 'content')
    
    def has_quiz(self, obj):
        return hasattr(obj, 'quiz')
    has_quiz.boolean = True
    has_quiz.short_description = 'Has Quiz'

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'article', 'points_per_question', 'question_count')
    inlines = [QuestionInline]
    
    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Number of Questions'
    
    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'

# We don't register Question as a standalone admin model
# It's only accessible through the Quiz admin
