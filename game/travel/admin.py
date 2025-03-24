#Authors: Nitzan Lahav, Michael Porter 

from django.contrib import admin
from .models import CampusTravel
# Register your models here.

@admin.register(CampusTravel)
class CampusTravelAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'travel_method', 'points', 'lat', 'lon')  
    list_filter = ('travel_method', 'date', 'points')  # Allow filtering by method, date, and points
    search_fields = ('user__username', 'travel_method')  # Enable quick searching
    date_hierarchy = 'date'  # Group by date for easier navigation
    ordering = ('-date', '-points')  # Show most recent and highest-scoring entries first
    readonly_fields = ('date',)  # Prevent edits to auto-created dates
    list_per_page = 20  # Manageable pagination size
    actions = ['reset_points', 'delete_entries']
    autocomplete_fields = ['user']  # Improve user selection for large datasets

    def get_queryset(self, request):
        # Optimize query to reduce DB hits
        qs = super().get_queryset(request)
        return qs.select_related('user')

    # Custom action to reset points to zero
    @admin.action(description="Reset points to zero for selected entries")
    def reset_points(self, request, queryset):
        updated = queryset.update(points=0)
        self.message_user(request, f"Successfully reset points for {updated} travel record(s).")

    # Custom action to delete selected entries
    @admin.action(description="Delete selected travel entries")
    def delete_entries(self, request, queryset):
        deleted, _ = queryset.delete()
        self.message_user(request, f"Successfully deleted {deleted} travel record(s).")

    # Override list display to include colored points
    def get_list_display(self, request):
        return ('user', 'date', 'travel_method', 'points_colored', 'lat', 'lon')

    # Format latitude and longitude for cleaner display
    def lat_lon_display(self, obj):
        if obj.lat is not None and obj.lon is not None:
            return f"({obj.lat:.5f}, {obj.lon:.5f})"
        return "N/A"
    lat_lon_display.short_description = "Location"
