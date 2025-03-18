#Authors: Nitzan Lahav, Michael Porter 

from django.contrib import admin
from .models import QRScan
from django.db import models

@admin.register(QRScan)
class QRScanAdmin(admin.ModelAdmin):
    list_display = ('user', 'scan_date', 'qr_code', 'points_earned', 'created_at')  # Keeps it clean and informative
    list_filter = ('scan_date', 'qr_code', 'points_earned')  # Add `points_earned` for more filtering options
    search_fields = ('user__username', 'qr_code')
    date_hierarchy = 'scan_date'
    ordering = ('-scan_date', '-created_at')  # Most recent scans at the top
    readonly_fields = ('created_at',)  # Prevent accidental edits to the creation date
    list_per_page = 20  # Paginate results to keep it manageable
    actions = ['reset_points', 'delete_scans']
    autocomplete_fields = ['user']  # Improves user selection for large user bases

    def get_queryset(self, request):
        # Optimize queryset to minimize DB hits and improve performance
        qs = super().get_queryset(request)
        return qs.select_related('user')

    # Custom action to reset points
    @admin.action(description="Reset points to zero for selected scans")
    def reset_points(self, request, queryset):
        updated = queryset.update(points_earned=0)
        self.message_user(request, f"Successfully reset points for {updated} scan(s).")

    # Custom action to delete scans
    @admin.action(description="Delete selected scans")
    def delete_scans(self, request, queryset):
        deleted, _ = queryset.delete()
        self.message_user(request, f"Successfully deleted {deleted} scan(s).")

    # Highlight high points earned
    def points_earned_colored(self, obj):
        color = "green" if obj.points_earned >= 10 else "red"
        return f'<span style="color: {color};">{obj.points_earned}</span>'
    points_earned_colored.allow_tags = True
    points_earned_colored.short_description = "Points Earned"

    # Override list display to show colored points
    def get_list_display(self, request):
        return ('user', 'scan_date', 'qr_code', 'points_earned_colored', 'created_at')
