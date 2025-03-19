# Author Tim Mishakov
import datetime
from django.shortcuts import render, redirect
from django.utils import timezone
from leaderboard.utils import update_leaderboard
from .models import CampusTravel

from profiles.models import Profile


def travel(request):
    if not request.user.is_authenticated:
        return redirect('login')

    today = timezone.localdate()

    # Check if the user already submitted today.
    if CampusTravel.objects.filter(user=request.user, date=today).exists():
        now = timezone.now()
        midnight = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        wait_seconds = (midnight - now).seconds
        hours = wait_seconds // 3600
        minutes = (wait_seconds % 3600) // 60
        wait_time = f"{hours} hours and {minutes} minutes" if hours else f"{minutes} minutes"

        last_submission = CampusTravel.objects.filter(user=request.user, date=today).latest('id')
        context = {
            'wait_time': wait_time,
            'last_submission_lat': last_submission.lat,
            'last_submission_lon': last_submission.lon,
        }
        return render(request, 'travel/already_submitted.html', context)

    if request.method == "POST":
        travel_method = request.POST.get('travel_method')
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        points_map = {
            "Walking": 30,
            "Biking": 20,
            "Car": 0,
            "Public transport": 5,
        }
        points = points_map.get(travel_method, 0)
        CampusTravel.objects.create(
            user=request.user,
            travel_method=travel_method,
            points=points,
            lat=lat,
            lon=lon 
        )
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.add_points(points)
        update_leaderboard(request.user, 'travel', points=points)
        context = {'points': points}
        return render(request, 'travel/thank_you.html', context)

    return render(request, 'travel/travel.html')
