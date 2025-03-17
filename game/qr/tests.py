from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from leaderboard.models import Leaderboard

class QRAppTests(TestCase):
    def setUp(self):
        """Create a test user"""

        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_get_qr_page(self):
        """Test that an authenticated GET request returns the QR scanning page."""

        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("qr_scan"))
        self.assertEqual(response.status_code, 200)
        # Ensure that the page contains text from the qr.html template
        self.assertContains(response, "QR Code Challenge")

    def test_post_valid_qr_code(self):
        """Test that posting a valid QR code updates the leaderboard and returns the success message."""

        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("qr_scan"), {"qr_code": "recycling_uni_bin"})
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(
            response,
            "Great job! You have earned 20 points for recycling!"
        )
        # Verify that the leaderboard entry for 'qr_scan' for this user has been updated to 20 points.
        entry = Leaderboard.objects.get(user=self.user, activity_type="qr_scan")
        self.assertEqual(entry.score, 20)

    def test_post_invalid_qr_code(self):
        """Test that posting an invalid QR code returns an error message and does not update the leaderboard."""

        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("qr_scan"), {"qr_code": "invalid_code"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid QR code. Please try again.")
        # Check that the leaderboard entry for 'qr_scan' either does not exist or remains at 0.
        try:
            entry = Leaderboard.objects.get(user=self.user, activity_type="qr_scan")
            self.assertEqual(entry.score, 0)
        except Leaderboard.DoesNotExist:
            # If no entry was created, that is acceptable.
            pass

    def test_requires_login(self):
        """Test that the QR endpoint requires the user to be logged in."""

        # Without login, the GET request should redirect to the login page.
        response = self.client.get(reverse("qr_scan"))
        self.assertEqual(response.status_code, 302)

    def test_one_entry_per_day(self):
        """Test that a user can only submit one qr code a day."""
        
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("qr_scan"), {"qr_code": "amory_uni_bin"})
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(
            response,
            "Great job! You have earned 20 points for recycling!"
        )

        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("qr_scan"), {"qr_code": "amory_uni_bin"})
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(
            response,
            "You've already scanned this QR code today. Come back tomorrow!"
        )

    def test_different_qr_codes_per_day(self):
        """Tests that a user can scan multiple different bins in one day."""

        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("qr_scan"), {"qr_code": "amory_uni_bin"})
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(
            response,
            "Great job! You have earned 20 points for recycling!"
        )

        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("qr_scan"), {"qr_code": "birks_uni_bin"})
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(
            response,
            "Great job! You have earned 20 points for recycling!"
        )