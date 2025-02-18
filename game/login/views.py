from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
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

    return render(request, "registration/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("/")  # Change to your actual dashboard/homepage URL
        else:
            messages.error(request, "Invalid password. Please try again.")
            print("DEBUG: Invalid password")  # Debugging

            if user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('home')  

         

        else:
            messages.error(request, "Invalid username or password. Please try again.")
    return render(request, "login.html")

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

