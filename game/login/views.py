# Authors: Michael Porter and Nitzan Lahav

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignupForm
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib import messages


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home or another page
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect("login")  # Redirect to login page after signup
    else:
        form = SignupForm()

    return render(request, "registration/signup.html", {"form": form})

#def login_view(request):
 #   if request.user.is_authenticated:
  #      return redirect('home')  # Redirect to home or another page
   # if request.method == "POST":
    #    form = AuthenticationForm(request, data=request.POST)
     ##   if form.is_valid():
       #     user = form.get_user()
        #    login(request, user)
         #   messages.success(request, "Login successful!")
            
            # Debugging: Print out the user's superuser status and username
          #  print(f"Logged in as: {user.username}, Superuser: {user.is_superuser}")
            
            # Check if the user is a superuser and redirect to admin
           # print(f"User: {user.username}, is_superuser: {user.is_superuser}")
##            if user.is_superuser:
  #              print("Redirecting to admin")
   #             return redirect('/admin/')
    #        else:
     #           print("Redirecting to home")
      #          return redirect('home')
       # else:
   #         messages.error(request, "Invalid username or password. Please try again.")
    #else:
     #   form = AuthenticationForm()

   # return render(request, "login.html", {"form": form})

class CustomLoginView(LoginView):
    def form_valid(self, form):
        """Override to add superuser redirect logic."""
        response = super().form_valid(form)  # Call the original LoginView logic
        user = self.request.user  # Get the logged-in user

        if user.is_superuser:
            messages.success(self.request, "Welcome, Admin! Redirecting to the admin panel.")
            return redirect('/admin/')  # Redirect superusers to admin

        return response  # Normal users proceed as usual

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def logout_view(request):
    logout(request)  # This logs out the user
    return redirect('/')  # Redirect to home or another page after logout