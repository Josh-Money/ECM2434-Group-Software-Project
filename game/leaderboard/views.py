# Author: Joshua Money
from django.shortcuts import render
from .models import Leaderboard
from django.db.models import Sum

def leaderboard(request):
    leaderboard_main = (
        Leaderboard.objects.values('user__username')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')[:10]
    )

    leaderboard_qr = (
        Leaderboard.objects.filter(activity_type='qr_scan')
        .values('user__username')
        .annotate(total_score=Sum('score'))
        .order_by('-score')[:10]
    )

    leaderboard_quiz = (
        Leaderboard.objects.filter(activity_type='quiz')
        .values('user__username')
        .annotate(total_score=Sum('score'))
        .order_by('-score')[:10]
    )
    
    leaderboard_travel = (
        Leaderboard.objects.filter(activity_type='travel')
        .values('user__username')
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