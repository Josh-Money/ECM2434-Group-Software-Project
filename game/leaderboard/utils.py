from leaderboard.models import Leaderboard

def update_leaderboard(user, activity_type, points):
    entry, created = Leaderboard.objects.get_or_create(
        user=user,
        activity_type=activity_type,
        defaults={'score': 0}
    )
    entry.score += points
    entry.save()