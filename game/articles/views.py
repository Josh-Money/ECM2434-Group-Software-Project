from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Article
from leaderboard.utils import update_leaderboard

# Create your views here.
@login_required
def articles(request):
    if request.method == 'POST':
        try:
            correct_count = int(request.POST.get('correct_answers', 0))
        except ValueError:
            correct_count = 0
        points_earned = 10 * correct_count

        update_leaderboard(request.user, 'quiz', points=points_earned)

        return JsonResponse({
            'points_earned': points_earned,
            'activity': 'quiz',
            'success': True
        })
    else:
        articles = Article.objects.all()
        return render(request, 'articles/articles.html', {'articles': articles})


    

