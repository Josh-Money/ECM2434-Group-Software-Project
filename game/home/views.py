# Author: Will Cooke and Tim Mishakov

from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from leaderboard.models import Leaderboard

def home(request):
    if not request.user.is_authenticated:
        return redirect('/')

    try: 
        user_entry = Leaderboard.objects.get(activity_type='leaderboard_main')
    except Leaderboard.DoesNotExist:
        user_entry = None

    request.session['username'] = request.user.username
    request.session['points'] = user_entry.score if user_entry else 0

    context = {
        'page_title': 'Home',
        'welcome_message': 'Welcome to the Home!',
        'description': 'Check out the latest posts and updates here.', 
        'user': {
            'name': request.user.username,
            'points': user_entry.score if user_entry else 0,
        }
    }
    return render(request, 'home/home.html', context)

