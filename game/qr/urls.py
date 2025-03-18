#Author: Joshua Money
from django.urls import path
from .views import scan_qr, qr_result

app_name = 'qr'

urlpatterns = [
    path('', scan_qr, name='qr_scan'),
    path('result/', qr_result, name='qr_result')
]