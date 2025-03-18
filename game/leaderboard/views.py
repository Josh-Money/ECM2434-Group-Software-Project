# Author: Joshua Money
from django.shortcuts import render, redirect
from .models import Leaderboard
from django.db.models import Sum
from django.core.paginator import Paginator

def leaderboard(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    # Get pagination parameters from request
    page_number = request.GET.get('page', 1)
    entries_per_page = request.GET.get('per_page', 10)
    
    # Validate entries_per_page (only allow 10, 25, or 50)
    if entries_per_page not in ['10', '25', '50']:
        entries_per_page = '10'
    
    # Convert to integer for use in queries
    entries_per_page_int = int(entries_per_page)
    
    activity_types = ['main', 'qr_scan', 'quiz', 'travel']
    user_scores = {}
    user_ranks = {}
    user_pages = {}

    for activity in activity_types:
        user_entry, created = Leaderboard.objects.get_or_create(
            user=request.user,
            activity_type=activity,
            defaults={'score': 0}
        )
        user_scores[activity] = user_entry.score
    
    # Get all leaderboard data for each activity type
    all_main_data = (
        Leaderboard.objects.values('user__username', 'user_id')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')
    )
    
    all_qr_data = (
        Leaderboard.objects.filter(activity_type='qr_scan')
        .values('user__username', 'user_id')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')
    )
    
    all_quiz_data = (
        Leaderboard.objects.filter(activity_type='quiz')
        .values('user__username', 'user_id')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')
    )
    
    all_travel_data = (
        Leaderboard.objects.filter(activity_type='travel')
        .values('user__username', 'user_id')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')
    )
    
    # Find user's rank in each leaderboard
    for i, entry in enumerate(all_main_data):
        if entry['user_id'] == request.user.id:
            user_ranks['main'] = i + 1
            user_pages['main'] = (i // entries_per_page_int) + 1
            break
    
    for i, entry in enumerate(all_qr_data):
        if entry['user_id'] == request.user.id:
            user_ranks['qr_scan'] = i + 1
            user_pages['qr_scan'] = (i // entries_per_page_int) + 1
            break
    
    for i, entry in enumerate(all_quiz_data):
        if entry['user_id'] == request.user.id:
            user_ranks['quiz'] = i + 1
            user_pages['quiz'] = (i // entries_per_page_int) + 1
            break
    
    for i, entry in enumerate(all_travel_data):
        if entry['user_id'] == request.user.id:
            user_ranks['travel'] = i + 1
            user_pages['travel'] = (i // entries_per_page_int) + 1
            break
    
    # Create paginators for each leaderboard
    paginator_main = Paginator(all_main_data, entries_per_page_int)
    paginator_qr = Paginator(all_qr_data, entries_per_page_int)
    paginator_quiz = Paginator(all_quiz_data, entries_per_page_int)
    paginator_travel = Paginator(all_travel_data, entries_per_page_int)
    
    # Get the requested page for each leaderboard
    leaderboard_main = paginator_main.get_page(page_number)
    leaderboard_qr = paginator_qr.get_page(page_number)
    leaderboard_quiz = paginator_quiz.get_page(page_number)
    leaderboard_travel = paginator_travel.get_page(page_number)
    
    # Prepare data for template
    context = {
        'username': request.user.username,
        'user_id': request.user.id,
        'user_main_score': user_scores['main'],
        'user_qr_score': user_scores['qr_scan'],
        'user_quiz_score': user_scores['quiz'],
        'user_travel_score': user_scores['travel'],
        'user_ranks': user_ranks,
        'user_pages': user_pages,
        'leaderboard_main': leaderboard_main,
        'leaderboard_qr': leaderboard_qr,
        'leaderboard_quiz': leaderboard_quiz,
        'leaderboard_travel': leaderboard_travel,
        'entries_per_page': entries_per_page,
        'page_number': int(page_number),
        'total_pages_main': paginator_main.num_pages,
        'total_pages_qr': paginator_qr.num_pages,
        'total_pages_quiz': paginator_quiz.num_pages,
        'total_pages_travel': paginator_travel.num_pages,
    }

    return render(request, 'leaderboard/leaderboard.html', context)