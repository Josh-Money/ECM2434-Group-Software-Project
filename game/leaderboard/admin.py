# Author: Joshua Money
from django.contrib import admin
from .models import Leaderboard

# Register your models here.

class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'score', 'created_at')
    list_filter = ('activity_type',)
    search_fields = ('user__username',)
    