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
from login.views import signup_view, privacy_policy #login_view
from django.contrib.auth.views import LogoutView
from leaderboard.views import leaderboard
from qr.views import scan_qr
from django.contrib.auth import views as auth_views
from login.views import logout_view, CustomLoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('home/', include('home.urls')),
    path("sign-up/", signup_view, name="signup"),
    path('logout/', logout_view, name='logout'),
    path('contact/', include('contact.urls')),
    path('leaderboard/', leaderboard, name="leaderboard"),
    path('articles/', include('articles.urls')),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('qr/', scan_qr, name="qr_scan"),
    path('challenges/', include('challenges.urls')),
    path('travel/', include('travel.urls')),
    path('profile/', include('profiles.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT or settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
