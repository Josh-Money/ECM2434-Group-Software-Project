from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import Profile, UserPointLog

User = get_user_model()

class UserPointLogInline(admin.TabularInline):
    model = UserPointLog
    extra = 0
    readonly_fields = ('points_added', 'timestamp')

class CustomUserAdmin(BaseUserAdmin):
    inlines = [UserPointLogInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'longest_streak', 'computed_rank')
    readonly_fields = ('computed_rank',)

    def computed_rank(self, obj):
        return obj.get_rank()
    computed_rank.short_description = 'Rank'
