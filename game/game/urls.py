"""
URL configuration for game project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from login.views import signup_view, privacy_policy
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
    path('contact/', include('contact.urls')),
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('articles/', include('articles.urls')),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("sign-up/", signup_view, name="signup"),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
]
