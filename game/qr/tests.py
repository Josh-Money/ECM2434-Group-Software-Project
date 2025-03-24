from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import QRScan
from datetime import timedelta

class QRScanTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        
        # Define test URLs
        self.qr_scan_url = reverse('qr:qr_scan')
        self.qr_result_url = reverse('qr:qr_result')
        
        # Define valid QR codes
        self.valid_qr_codes = {
            "birks_uni_bin": 20,
            "forum_bin": 20,
            "library_bin": 20
        }

    def test_qr_scan_page_loads(self):
        """Test that the QR scan page loads correctly"""
        response = self.client.get(self.qr_scan_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qr/qr.html')

    def test_qr_result_page_loads(self):
        """Test that the QR result page loads correctly"""
        response = self.client.get(self.qr_result_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qr/qr_result.html')

    def test_valid_qr_scan(self):
        """Test scanning a valid QR code"""
        qr_code = "birks_uni_bin"
        response = self.client.post(self.qr_scan_url, {'qr_code': qr_code})
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qr/qr_result.html')
        
        # Check if QR scan was recorded
        qr_scan = QRScan.objects.get(user=self.user, qr_code=qr_code)
        self.assertEqual(qr_scan.points_earned, self.valid_qr_codes[qr_code])

    def test_invalid_qr_scan(self):
        """Test scanning an invalid QR code"""
        response = self.client.post(self.qr_scan_url, {'qr_code': 'invalid_qr'})
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qr/qr_result.html')
        self.assertIn('Invalid QR code', response.context['message'])

    def test_duplicate_qr_scan_same_day(self):
        """Test that users cannot scan the same QR code twice in one day"""
        qr_code = "birks_uni_bin"
        
        # First scan
        self.client.post(self.qr_scan_url, {'qr_code': qr_code})
        
        # Second scan
        response = self.client.post(self.qr_scan_url, {'qr_code': qr_code})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('already scanned this QR code today', response.context['message'])
        
        # Verify only one scan was recorded
        self.assertEqual(QRScan.objects.filter(user=self.user, qr_code=qr_code).count(), 1)

    def test_qr_scan_different_days(self):
        """Test that users can scan the same QR code on different days"""
        qr_code = "birks_uni_bin"
        
        # First scan
        self.client.post(self.qr_scan_url, {'qr_code': qr_code})
        
        # Modify the scan date to yesterday
        qr_scan = QRScan.objects.get(user=self.user, qr_code=qr_code)
        qr_scan.scan_date = timezone.now().date() - timedelta(days=1)
        qr_scan.save()
        
        # Second scan
        response = self.client.post(self.qr_scan_url, {'qr_code': qr_code})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.context['status'])
        
        # Verify two scans were recorded
        self.assertEqual(QRScan.objects.filter(user=self.user, qr_code=qr_code).count(), 2)

    def test_qr_scan_empty_code(self):
        """Test submitting an empty QR code"""
        response = self.client.post(self.qr_scan_url, {'qr_code': ''})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid QR code', response.context['message'])

    def test_qr_scan_missing_code(self):
        """Test submitting without a QR code"""
        response = self.client.post(self.qr_scan_url, {})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid QR code', response.context['message'])
        
