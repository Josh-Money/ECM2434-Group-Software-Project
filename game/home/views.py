# Authors: Will Cooke (challenges + events) and Tim Mishakov (leaderboard)

from django.shortcuts import render, redirect
from leaderboard.models import Leaderboard
from django.db.models import Sum 
from .models import Event
from django.utils import timezone

def home(request):
    # Get all leaderboard data ordered by score
    all_leaderboard_data = (
        Leaderboard.objects.values('user__username', 'user_id')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')
    )

    # Get top 3 entries
    top_3_data = list(all_leaderboard_data[:3])
    
    # Find current user's position and data
    user_position = None
    user_data = None
    
    for i, entry in enumerate(all_leaderboard_data):
        if request.user.is_authenticated and entry['user_id'] == request.user.id:
            user_position = i
            user_data = entry
            break
    
    # Prepare leaderboard list with top 3 and current user
    leaderboard_list = []
    
    # Calculate max score for progress bar
    max_score = top_3_data[0]['total_score'] if top_3_data else 0
    
    # Add top 3 to the list with their ranks
    for i, entry in enumerate(top_3_data):
        username = entry['user__username']
        score = entry['total_score']
        progress = (score / max_score * 100) if max_score > 0 else 0
        rank = i + 1  # 1-indexed rank
        
        leaderboard_list.append({
            'name': username,
            'points': score,
            'progress': round(progress),
            'position': rank,
            'is_current_user': request.user.is_authenticated and username == request.user.username
        })
    
    # Add current user if not in top 3 and user is authenticated
    if request.user.is_authenticated and user_position is not None and user_position >= 3:
        # Add ellipsis entry
        leaderboard_list.append({
            'name': '...',
            'points': '...',
            'progress': 0,
            'is_ellipsis': True
        })
        
        # Add current user
        score = user_data['total_score']
        progress = (score / max_score * 100) if max_score > 0 else 0
        leaderboard_list.append({
            'name': user_data['user__username'],
            'points': score,
            'progress': round(progress),
            'is_current_user': True,
            'position': user_position + 1  # +1 because position is 0-indexed
        })

    # Get upcoming events
    upcoming_events = Event.objects.filter(
        date__gte=timezone.now().date()
    ).order_by('date', 'time')[:5]  # Show max 5 upcoming events

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
        'events': upcoming_events,
    }
    return render(request, 'home/home.html', context)

