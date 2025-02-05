#Author: Joshua Money
from django.urls import path 
from .views import leaderboard

urlpatterns = [
    path('', leaderboard, name='leaderboard'),
]