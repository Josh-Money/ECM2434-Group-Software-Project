from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def home(request):
    # Debug logging (optional)
    print('User:', request.user)
    print('Username:', request.user.username)
    print('Is Authenticated:', request.user.is_authenticated)


    if not request.user.is_authenticated:
        return redirect('login')  

    real_users = User.objects.exclude(username__startswith='testuser')

    leaderboard = []
    for user in real_users:
        points = 0         
        progress = points   
        leaderboard.append({
            'name': user.username,
            'points': points,
            'progress': progress,
        })

    # Sort the leaderboard by points (highest first) and limit to top 10
    leaderboard = sorted(leaderboard, key=lambda x: x['points'], reverse=True)[:10]

    context = {
        'page_title': 'Home',
        'welcome_message': 'Welcome to the Home!',
        'description': 'Check out the latest posts and updates here.',
        'user': {
            'name': request.user.username,
            'points': 0  
        },
        'leaderboard': leaderboard,
    }
    return render(request, 'home/home.html', context)
