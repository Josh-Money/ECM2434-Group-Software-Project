# Author: Joshua Money
from django.shortcuts import render
from .models import Score
from django.db.models import Sum

def leaderboard(request):
    leaderboard_main = (
        Score.objects.values('player_name')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')[:10]
    )

    leaderboard_qr = (
        Score.objects.filter(activity_type='qr_scan')
        .values('player_name')
        .annotate(total_score=Sum('score'))
        .order_by('-score')[:10]
    )

    leaderboard_quiz = (
        Score.objects.filter(activity_type='quiz')
        .values('player_name')
        .annotate(total_score=Sum('score'))
        .order_by('-score')[:10]
    )
    
    leaderboard_travel = (
        Score.objects.filter(activity_type='travel')
        .values('player_name')
        .annotate(total_score=Sum('score'))
        .order_by('-score')[:10]
    )

    context = {
        'leaderboard_main': leaderboard_main,
        'leaderboard_qr': leaderboard_qr,
        'leaderboard_quiz': leaderboard_quiz,
        'leaderboard_travel': leaderboard_travel,
    }

    return render(request, 'leaderboard/leaderboard.html', context)