from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Article, Quiz, Question
from leaderboard.utils import update_leaderboard

# Create your views here.
@login_required
def articles(request):
    if request.method == 'POST':
        try:
            quiz_id = int(request.POST.get('quiz_id', 0))
            correct_count = int(request.POST.get('correct_answers', 0))
        except ValueError:
            return JsonResponse({'error': 'Invalid data'}, status=400)
        
        quiz = get_object_or_404(Quiz, id=quiz_id)
        points_earned = quiz.points_per_question * correct_count

        update_leaderboard(request.user, 'quiz', points=points_earned)

        return JsonResponse({'points_earned': points_earned})
    else:
        articles = Article.objects.all()
        return render(request, 'articles/articles.html', {'articles': articles})

# This view is no longer used in the single-page approach
# @login_required
# def article_detail(request, article_id):
#     article = get_object_or_404(Article, id=article_id)
#     try:
#         quiz = article.quiz
#         questions = quiz.questions.all()
#     except Quiz.DoesNotExist:
#         quiz = None
#         questions = []
#         
#     context = {
#         'article': article,
#         'quiz': quiz,
#         'questions': questions,
#     }
#     return render(request, 'articles/article_detail.html', context)

@login_required
def get_question_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return JsonResponse({
        'correct_answer': question.correct_answer
    })


    

