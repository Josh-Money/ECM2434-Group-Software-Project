# Author: Joshua Money
from django.contrib import admin
from .models import Score

# Register your models here.

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('player_name', 'activity_type', 'score', 'created_at')
    list_filter = ('activity_type',)
    search_fields = ('player_name',)
    