# Author: Will Cooke

from django.shortcuts import render

def home(request):
    # Determine the name to display for the current user
    user_name = request.user.username if request.user.is_authenticated else "Guest"
    
    # Build the leaderboard.
    # If your User model (or a related Profile) has a points attribute, use that.
    # For demonstration, we assume each user has a "points" attribute or default to 100.
    leaderboard = []
    users = User.objects.all()  # In production, you might want to order this by points.
    for user in users:
        # If you have extended the User model or have a profile with points, do something like:
        # points = user.profile.points
        # For demonstration, we'll check if the user has an attribute 'points', otherwise use 100.
        points = getattr(user, 'points', 100)
        leaderboard.append({
            'name': user.username,
            'points': points,
        })
    
    # Optionally, sort the leaderboard in descending order by points
    leaderboard = sorted(leaderboard, key=lambda x: x['points'], reverse=True)
    
    context = {
        'page_title': 'Home',
        'welcome_message': 'Welcome to the Home!',
        'description': 'Check out the latest posts and updates here.',
        'user_info': {
            'name': user_name,
            # Here you can also pull the logged-in user’s points from a session or their profile.
            'points': request.session.get('points', 0)  # Or, e.g., request.user.profile.points if available.
        },
        'leaderboard': leaderboard,
    }
    return render(request, 'home/home.html', context)

#def post_detail(request, id):
#    return render(request, 'home/post_detail.html', {'post_id': id})