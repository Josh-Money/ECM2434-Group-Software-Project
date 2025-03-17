from django.contrib import admin
from .models import QRScan

@admin.register(QRScan)
class QRScanAdmin(admin.ModelAdmin):
    list_display = ('user', 'scan_date', 'qr_code', 'points_earned', 'created_at')
    list_filter = ('scan_date', 'qr_code')
    search_fields = ('user__username', 'qr_code')
    date_hierarchy = 'scan_date'