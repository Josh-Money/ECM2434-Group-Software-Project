from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def home(request):
    # Debug logging (optional)
    print('User:', request.user)
    print('Username:', request.user.username)
    print('Is Authenticated:', request.user.is_authenticated)

    # Redirect unauthenticated users (adjust redirect URL as needed)
    if not request.user.is_authenticated:
        return redirect('login')  # Replace 'login' with your actual login URL name

    # Query real users by excluding dummy test users (those whose username starts with "testuser")
    real_users = User.objects.exclude(username__startswith='testuser')

    leaderboard = []
    # For each real user, assign a points value.
    # Replace this default with your actual logic to get a user's points (e.g., from a profile model).
    for user in real_users:
        points = 0          # Default points; replace with e.g., user.profile.points
        progress = points   # For demonstration, progress equals points
        leaderboard.append({
            'name': user.username,
            'points': points,
            'progress': progress,
        })

    # Sort the leaderboard by points (highest first) and limit to top 10
    leaderboard = sorted(leaderboard, key=lambda x: x['points'], reverse=True)[:10]

    # Build the context with your welcome details and the leaderboard data
    context = {
        'page_title': 'Home',
        'welcome_message': 'Welcome to the Home!',
        'description': 'Check out the latest posts and updates here.',
        'user': {
            'name': request.user.username,
            'points': 0  # Replace with actual points if available
        },
        'leaderboard': leaderboard,
    }
    return render(request, 'home/home.html', context)
