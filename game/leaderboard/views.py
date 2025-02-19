# Author: Joshua Money
from django.shortcuts import render, redirect
from .models import Leaderboard
from django.db.models import Sum

def leaderboard(request):

    if not request.user.is_authenticated:
        return redirect('/')
    
    activity_types = ['main', 'qr_scan', 'quiz', 'travel']
    user_scores = {}

    for activity in activity_types:
        user_entry, created = Leaderboard.objects.get_or_create(
            user=request.user,
            activity_type = activity,
            defaults={'score': 0}
        )
        user_scores[activity] = user_entry.score
    
    leaderboard_main = (
        Leaderboard.objects.filter(activity_type='main')
        .values('user__username')
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
        'username': request.user.username,
        'user_main_score': user_scores['main'],
        'user_qr_score': user_scores['qr_scan'],
        'user_quiz_score': user_scores['quiz'],
        'user_travel_score': user_scores['travel'],
        'leaderboard_main': leaderboard_main,
        'leaderboard_qr': leaderboard_qr,
        'leaderboard_quiz': leaderboard_quiz,
        'leaderboard_travel': leaderboard_travel,
    }

    return render(request, 'leaderboard/leaderboard.html', context)