from django.db.models import Sum
from django.utils.html import format_html
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
        # Apply score filtering only to allowed activity types
        allowed_types = ['travel', 'qr_scan', 'quiz']
        queryset = queryset.filter(activity_type__in=allowed_types)

        if self.value() == 'low':
            return queryset.filter(score__range=(0, 100))
        if self.value() == 'medium':
            return queryset.filter(score__range=(101, 500))
        if self.value() == 'high':
            return queryset.filter(score__gt=500)
        return queryset

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

class ActivityTypeFilter(SimpleListFilter):
    title = 'Activity Type'
    parameter_name = 'activity_type'

    def lookups(self, request, model_admin):
        # Exclude 'main' from the available filter options
        return [
            ('qr_scan', 'QR Scan'),
            ('quiz', 'Quiz'),
            ('travel', 'Travel'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(activity_type=self.value())
        return queryset

class LeaderboardAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'score', 'total_score', 'created_at') 
    list_filter = (ActivityTypeFilter, ScoreRangeFilter)  # Use custom activity type filter
    search_fields = ('user__username',)
    ordering = ('-score', '-created_at')
    date_hierarchy = 'created_at'
    list_editable = ('score',)
    actions = [reset_scores, double_scores, remove_inactive_users]

    # Sum points from 'travel', 'qr_scan', and 'quiz' only
    def total_score(self, obj):
        total = Leaderboard.objects.filter(
            user=obj.user,
            activity_type__in=['travel', 'qr_scan', 'quiz']  # Exclude 'main'
        ).aggregate(total=Sum('score'))['total'] or 0
        
        color = "green" if total >= 500 else "red"
        return format_html('<span style="color: {};">{}</span>', color, total)
    
    total_score.short_description = "Total Score"

    def get_queryset(self, request):
        # Exclude 'main' from the queryset entirely
        qs = super().get_queryset(request)
        qs = qs.select_related('user').exclude(activity_type='main')
        return qs
    
admin.site.register(Leaderboard, LeaderboardAdmin)
