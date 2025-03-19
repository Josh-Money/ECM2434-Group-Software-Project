from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth import get_user_model
from leaderboard.models import Leaderboard
from .forms import ProfileImageForm

User = get_user_model()

@login_required
def profile_view(request, username=None):
    """
    Displays the profile for the specified 'username'.
    If no username is provided, it shows the logged-in user's profile.
    """
    # If no username in the URL, use the logged-in user
    if username is None:
        profile_user = request.user
    else:
        # Otherwise, get the user matching 'username'
        profile_user = get_object_or_404(User, username=username)

    # Calculate total score for profile_user
    total_score = Leaderboard.objects.filter(user=profile_user).aggregate(
        total=Sum('score')
    )['total'] or 0

    # Calculate rank
    user_scores = Leaderboard.objects.values('user').annotate(total=Sum('score'))
    # Sort by score descending
    ordered_users = sorted(user_scores, key=lambda x: x['total'], reverse=True)
    ordered_ids = [entry['user'] for entry in ordered_users]

    try:
        rank = ordered_ids.index(profile_user.id) + 1
    except ValueError:
        rank = "N/A"

    context = {
        'profile_user': profile_user,
        'total_score': total_score,
        'rank': rank,
    }
    return render(request, 'profiles/profile.html', context)

@login_required
def update_profile_picture(request):
    """
    Allows the currently logged-in user (request.user) to update their profile picture.
    """
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileImageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Redirect to the logged-in user's profile
            return redirect('profile_detail', username=request.user.username)
    else:
        form = ProfileImageForm(instance=profile)
    return render(request, 'profiles/update_picture.html', {'form': form})
