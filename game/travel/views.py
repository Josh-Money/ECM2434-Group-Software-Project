import datetime
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import CampusTravel

def travel(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Use timezone.localdate() for the current day.
    today = timezone.localdate()

    # Check if the user already submitted today.
    if CampusTravel.objects.filter(user=request.user, date=today).exists():
        now = timezone.now()
        # Compute midnight of the next day.
        midnight = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        wait_seconds = (midnight - now).seconds
        hours = wait_seconds // 3600
        minutes = (wait_seconds % 3600) // 60
        if hours:
            wait_time = f"{hours} hours and {minutes} minutes"
        else:
            wait_time = f"{minutes} minutes"
        context = {
            'wait_time': wait_time,
        }
        return render(request, 'travel/already_submitted.html', context)

    if request.method == "POST":
        travel_method = request.POST.get('travel_method')
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
            points=points
        )
        context = {'points': points}
        return render(request, 'travel/thank_you.html', context)

    # GET request: Render the travel (submission) page.
    return render(request, 'travel/travel.html')
