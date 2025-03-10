import datetime
from django.shortcuts import render, redirect
from .models import CampusTravel

def travel(request):
    if not request.user.is_authenticated:
        return redirect('login')

    today = datetime.date.today()
    # If the user has already submitted today, show an info page
    if CampusTravel.objects.filter(user=request.user, date=today).exists():
        return render(request, 'travel/already_submitted.html')

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
        return render(request, 'travel/thank_you.html')

    # GET request: render the form page
    return render(request, 'travel/travel.html')
