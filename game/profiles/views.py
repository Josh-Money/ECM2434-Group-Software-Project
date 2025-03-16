from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from leaderboard.models import Leaderboard 

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
