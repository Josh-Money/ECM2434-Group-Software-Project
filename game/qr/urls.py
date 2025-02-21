#Author: Joshua Money
from django.urls import path
from .views import scan_qr

app_name = 'qr'

urlpatterns = [
    path('', scan_qr, name='qr_scan')
]