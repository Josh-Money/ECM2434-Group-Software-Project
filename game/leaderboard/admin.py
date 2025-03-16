# Author: Joshua Money
from django.contrib import admin
from .models import Leaderboard

# Register your models here.

#class LeaderboardAdmin(admin.ModelAdmin):
 #   list_display = ('user', 'activity_type', 'score', 'created_at')
  #  list_filter = ('activity_type',)
   # search_fields = ('user__username',)

#admin.site.register(Leaderboard, LeaderboardAdmin)

from django.contrib import admin
from .models import Leaderboard
from django.contrib.admin import SimpleListFilter
from import_export.admin import ExportMixin

class ScoreRangeFilter(SimpleListFilter):
    title = 'Score Range'
    parameter_name = 'score_range'

    def lookups(self, request, model_admin):
        return [
            ('low', '0-100'),
            ('medium', '101-500'),
            ('high', '501+'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(score__range=(0, 100))
        if self.value() == 'medium':
            return queryset.filter(score__range=(101, 500))
        if self.value() == 'high':
            return queryset.filter(score__gt=500)

@admin.action(description="Reset selected scores to zero")
def reset_scores(modeladmin, request, queryset):
    queryset.update(score=0)

@admin.action(description="Double selected scores")
def double_scores(modeladmin, request, queryset):
    for obj in queryset:
        obj.score *= 2
        obj.save()

@admin.action(description="Remove selected leaderboard entries for inactive users")
def remove_inactive_users(modeladmin, request, queryset):
    queryset.filter(user__is_active=False).delete()

class LeaderboardAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'score', 'created_at')
    list_filter = ('activity_type', ScoreRangeFilter)
    search_fields = ('user__username',)
    ordering = ('-score', '-created_at')
    date_hierarchy = 'created_at'
    list_editable = ('score',)
    actions = [reset_scores, double_scores, remove_inactive_users]

admin.site.register(Leaderboard, LeaderboardAdmin)
