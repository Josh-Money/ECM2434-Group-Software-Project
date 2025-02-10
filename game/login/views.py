from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignupForm

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect("login")  # Redirect to login page after signup
    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        print(f"DEBUG: Attempting login with username: {username}")  # Debugging

        # Check if the username exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, "User does not exist. Please sign up first.")
            print("DEBUG: User not found, redirecting to signup")  # Debugging
            return redirect("signup")  # Make sure 'signup' is the correct URL name

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("dashboard")  # Change to your actual dashboard/homepage URL
        else:
            messages.error(request, "Invalid password. Please try again.")
            print("DEBUG: Invalid password")  # Debugging

    return render(request, "login.html")

