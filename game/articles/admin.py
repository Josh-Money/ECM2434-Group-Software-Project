from django.contrib import admin
from .models import Article, Quiz, Question

# Register your models here.
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 5

class QuizInline(admin.StackedInline):
    model = Quiz
    can_delete = False
    show_change_link = True

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'has_quiz')
    search_fields = ('title', 'content')
    inlines = [QuizInline]
    
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

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'correct_answer', 'order')
    list_filter = ('quiz', 'correct_answer')
    ordering = ('quiz', 'order')
