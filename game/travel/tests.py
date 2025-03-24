# campus_tracker/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

from .models import CampusTravel

class CampusTrackerTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="password", email="test@example.com"
        )
        self.url = reverse("travel")

    def test_get_travel_page_when_not_submitted(self):
        """Test that a logged-in user who has not submitted today gets the travel page."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "travel/travel.html")

    def test_post_submission_creates_record_and_shows_thank_you(self):
        """Test that a POST submission creates a record and returns the thank you page."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(self.url, {"travel_method": "Walking"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "travel/thank_you.html")

        # Verify that a CampusTravel record was created with the correct points.
        today = timezone.localdate()
        submission = CampusTravel.objects.filter(user=self.user, date=today).first()
        self.assertIsNotNone(submission)
        self.assertEqual(submission.travel_method, "Walking")
        self.assertEqual(submission.points, 30)
        # Checks that the thank you page includes the points earned.
        self.assertContains(response, "30")

    def test_get_already_submitted_page(self):
        """Test that if a submission exists for today, the already_submitted page is shown."""
        self.client.login(username="testuser", password="password")
        # Create a submission for today
        today = timezone.localdate()
        CampusTravel.objects.create(
            user=self.user, travel_method="Biking", points=20
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "travel/already_submitted.html")
        # Verify that the already_submitted page includes a message about waiting.
        self.assertContains(response, "Submission Received")
        self.assertContains(response, "Please wait")
