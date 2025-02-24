# Author: Will Cooke and Tim Mishakov

from django.shortcuts import render, redirect
from leaderboard.models import Leaderboard
from django.db.models import Sum 

def home(request):
    leaderboard_data = (
        Leaderboard.objects.values('user__username')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')[:10]
    )

    leaderboard_list = []
    if leaderboard_data:
        max_score = leaderboard_data[0]['total_score']
    else:
        max_score = 0

    for entry in leaderboard_data:
        username = entry['user__username']
        score = entry['total_score']
        progress = (score / max_score * 100) if max_score > 0 else 0
        leaderboard_list.append({
            'name': username,
            'points': score,
            'progress': round(progress),
        })

    user_total = Leaderboard.objects.filter(user=request.user).aggregate(total=Sum('score'))['total'] or 0

    context = {
        'page_title': 'Home',
        'welcome_message': 'Welcome to the Home!',
        'description': 'Check out the latest posts and updates here.', 
        'user': {
            'name': request.user.username,
            'points': user_total,
        },
        'leaderboard': leaderboard_list,
    }
    return render(request, 'home/home.html', context)

