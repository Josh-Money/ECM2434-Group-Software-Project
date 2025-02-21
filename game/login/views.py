# Authors: Michael Porter and Nitzan Lahav

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignupForm
from django.contrib.auth import logout
from django.shortcuts import redirect

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect("login")  # Redirect to login page after signup
    else:
        form = SignupForm()

    return render(request, "registration/signup.html", {"form": form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            
            # Debugging: Print out the user's superuser status and username
            print(f"Logged in as: {user.username}, Superuser: {user.is_superuser}")
            
            # Check if the user is a superuser and redirect to admin
            if user.is_superuser:
                
                return redirect('/admin/')
            else:
                print("Redirecting to home")
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})



def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def logout_view(request):
    logout(request)  # This logs out the user
    return redirect('/')  # Redirect to home or another page after logout