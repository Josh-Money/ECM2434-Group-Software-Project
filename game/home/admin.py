from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'date', 'time', 'is_past')
    list_filter = ('date', 'location')
    search_fields = ('title', 'location', 'description')
    date_hierarchy = 'date'
    
    def is_past(self, obj):
        return obj.is_past
    is_past.boolean = True
    is_past.short_description = 'Past Event'
