from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from leaderboard.models import Leaderboard

class QRAppTests(TestCase):
    def setUp(self):
        """Make a test user"""

        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_get_qr_page(self):
        """Check if the QR scanning page loads for logged in users."""

        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("qr_scan"))
        self.assertEqual(response.status_code, 200)
        # Check if the page has the right title
        self.assertContains(response, "QR Code Challenge")

    def test_post_valid_qr_code(self):
        """Check if scanning a valid QR code gives points and shows success message."""

        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("qr_scan"), {"qr_code": "recycling_uni_bin"})
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(
            response,
            "Great job! You have earned 20 points for recycling!"
        )
        # Check if points were added to leaderboard
        entry = Leaderboard.objects.get(user=self.user, activity_type="qr_scan")
        self.assertEqual(entry.score, 20)

    def test_scan_same_qr_code_twice(self):
        """Check if scanning the same QR code twice doesn't give points twice."""
        
        self.client.login(username="testuser", password="testpass")
        
        # First scan - should give points
        response1 = self.client.post(reverse("qr_scan"), {"qr_code": "recycling_uni_bin"})
        self.assertEqual(response1.status_code, 200)
        self.assertContains(response1, "Great job! You have earned 20 points for recycling!")
        
        # Check points after first scan
        entry1 = Leaderboard.objects.get(user=self.user, activity_type="qr_scan")
        self.assertEqual(entry1.score, 20)
        
        # Second scan - should not give more points
        response2 = self.client.post(reverse("qr_scan"), {"qr_code": "recycling_uni_bin"})
        self.assertEqual(response2.status_code, 200)
        # Check for the exact message with HTML entity for apostrophe
        self.assertContains(response2, "You&#x27;ve already scanned a QR code today")
        
        # Check points after second scan - should still be 20
        entry2 = Leaderboard.objects.get(user=self.user, activity_type="qr_scan")
        self.assertEqual(entry2.score, 20)

    def test_post_invalid_qr_code(self):
        """Check if scanning an invalid QR code shows error and doesn't give points."""

        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("qr_scan"), {"qr_code": "invalid_code"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid QR code. Please try again.")
        # Make sure no points were added
        try:
            entry = Leaderboard.objects.get(user=self.user, activity_type="qr_scan")
            self.assertEqual(entry.score, 0)
        except Leaderboard.DoesNotExist:
            # It's fine if no entry was created
            pass

    def test_requires_login(self):
        """Check if you need to be logged in to scan QR codes."""

        # Should redirect to login if not logged in
        response = self.client.get(reverse("qr_scan"))
        self.assertEqual(response.status_code, 302)
