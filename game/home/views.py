# Author: Will Cooke and Tim Mishakov

from django.shortcuts import render
from django.contrib.auth.models import User

def create_test_users():
    """
    Create 10 test users (if they do not exist already) with usernames testuser1 ... testuser10.
    """
    for i in range(10):
        username = f"testuser{i+1}"
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password="password")

def home(request):
    create_test_users()
    leaderboard = []
    for i in range(10):
        username = f"testuser{i+1}"
        points = 100 - i * 10   
        progress = points       
        leaderboard.append({
            'name': username,
            'points': points,
            'progress': progress,
        })
    
    context = {
        'page_title': 'Home',
        'leaderboard': leaderboard,
    }
    return render(request, 'home/home.html', context)
