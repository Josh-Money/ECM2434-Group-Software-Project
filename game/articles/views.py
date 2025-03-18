from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Article
from leaderboard.utils import update_leaderboard
from profiles.models import Profile


# Create your views here.
@login_required
def articles(request):
    if request.method == 'POST':
        try:
            correct_count = int(request.POST.get('correct_answers', 0))
        except ValueError:
            correct_count = 0
        points_earned = 10 * correct_count

        # Updating profile
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.add_points(points_earned)


        update_leaderboard(request.user, 'quiz', points=points_earned)

        return JsonResponse({'points_earned': points_earned})
    else:
        articles = Article.objects.all()
        return render(request, 'articles/articles.html', {'articles': articles})


    

