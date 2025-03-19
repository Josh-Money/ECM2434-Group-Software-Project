from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from leaderboard.models import Leaderboard 
from .forms import ProfileImageForm

@login_required
def profile_view(request):
    user = request.user

    # Calculate total score
    total_score = Leaderboard.objects.filter(user=user).aggregate(total=Sum('score'))['total'] or 0

    # Calculate rank
    user_scores = Leaderboard.objects.values('user').annotate(total=Sum('score'))
    # Sort by score descending
    ordered_users = [entry['user'] for entry in sorted(user_scores, key=lambda x: x['total'], reverse=True)]

    try:
        rank = ordered_users.index(user.id) + 1
    except ValueError:
        rank = "N/A"

    context = {
        'total_score': total_score,
        'rank': rank,
    }
    return render(request, 'profiles/profile.html', context)

@login_required
def update_profile_picture(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileImageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to a profile view
    else:
        form = ProfileImageForm(instance=profile)
    return render(request, 'profiles/update_picture.html', {'form': form})