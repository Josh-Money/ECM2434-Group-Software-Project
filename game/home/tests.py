# Authors: Will Cooke and Tim Mishakov

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from leaderboard.models import Leaderboard
from .models import Event
from django.utils import timezone
from datetime import datetime, timedelta

class HomeViewTest(TestCase):
    
    def setUp(self):
        """Set up a test client and test users with leaderboard entries."""
        self.client = Client()
        # Create the primary user for authentication.
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a leaderboard entry for the primary user with a score of 100.
        Leaderboard.objects.create(user=self.user, score=100)
        
        # Create additional users and their leaderboard entries.
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.user3 = User.objects.create_user(username='user3', password='password123')
        Leaderboard.objects.create(user=self.user2, score=200)
        Leaderboard.objects.create(user=self.user3, score=150)
    
    def test_home_renders_for_authenticated_user(self):
        """Test if authenticated users can access the home page."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')

    def test_home_context_contains_user_data(self):
        """Test if the home page context contains user data."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'testuser')
        self.assertContains(response, '100')
    
    def test_leaderboard_section_renders_correctly(self):
        """Test that the leaderboard section renders with correct ordering and progress."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        content = response.content.decode('utf-8')
        # Check that the leaderboard container and header are present.
        self.assertIn('<div class="leaderboard-container">', content)
        self.assertIn('<h4 class="subtitle">Leaderboard</h4>', content)
        
        # The aggregation in the view orders entries as:
        #   user2: score=200 => progress: 200/200*100 = 100%
        #   user3: score=150 => progress: 150/200*100 = 75%
        #   testuser: score=100 => progress: 100/200*100 = 50%
        self.assertIn('user2', content)
        self.assertIn('200', content)
        self.assertIn('style="width: 100%"', content)
        
        self.assertIn('user3', content)
        self.assertIn('150', content)
        self.assertIn('style="width: 75%"', content)
        
        self.assertIn('testuser', content)
        self.assertIn('100', content)
        self.assertIn('style="width: 50%"', content)
        
    
    def test_leaderboard_empty(self):
        """Test that the empty leaderboard message is shown when no leaderboard data exists."""
        # Remove all leaderboard entries.
        Leaderboard.objects.all().delete()
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No leaderboard data available.')

class EventModelTest(TestCase):
    
    def test_event_creation(self):
        """Test that events can be created with proper attributes."""
        event = Event.objects.create(
            title='Sustainability Workshop',
            location='Amory Building',
            date=timezone.now().date(),
            time=timezone.now().time(),
            description='Learn about sustainability practices',
            subscription='Register at reception'
        )
        self.assertEqual(event.title, 'Sustainability Workshop')
        self.assertEqual(event.location, 'Amory Building')
        self.assertEqual(event.description, 'Learn about sustainability practices')
        self.assertEqual(event.subscription, 'Register at reception')
        
    def test_event_string_representation(self):
        """Test the string representation of an event."""
        event = Event.objects.create(
            title='Campus Clean-up',
            location='Forum',
            date=timezone.now().date(),
            time=timezone.now().time(),
            description='Help clean the campus'
        )
        self.assertEqual(str(event), 'Campus Clean-up')
        
    def test_is_past_property_future_event(self):
        """Test that is_past property correctly identifies future events."""
        tomorrow = timezone.now() + timedelta(days=1)
        event = Event.objects.create(
            title='Future Workshop',
            location='Innovation Centre',
            date=tomorrow.date(),
            time=tomorrow.time(),
            description='Planning for the future'
        )
        self.assertFalse(event.is_past)
        
    def test_is_past_property_past_event(self):
        """Test that is_past property correctly identifies past events."""
        yesterday = timezone.now() - timedelta(days=1)
        event = Event.objects.create(
            title='Past Workshop',
            location='Innovation Centre',
            date=yesterday.date(),
            time=yesterday.time(),
            description='Past planning session'
        )
        self.assertTrue(event.is_past)
        
    def test_event_with_no_subscription(self):
        """Test that events can be created without subscription information."""
        event = Event.objects.create(
            title='Open House',
            location='Student Guild',
            date=timezone.now().date(),
            time=timezone.now().time(),
            description='Open to all students'
        )
        self.assertEqual(event.subscription, None)
        
    def test_event_date_time_formatting(self):
        """Test that event date and time are stored correctly."""
        test_date = timezone.now().date()
        test_time = timezone.now().time()
        
        event = Event.objects.create(
            title='Time Test Event',
            location='Clock Tower',
            date=test_date,
            time=test_time,
            description='Testing date/time storage'
        )
        
        self.assertEqual(event.date, test_date)
        self.assertEqual(event.time, test_time)
        
class EventsInHomeViewTest(TestCase):
    
    def setUp(self):
        """Set up test client, user, and events."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create future events
        tomorrow = timezone.now() + timedelta(days=1)
        self.event1 = Event.objects.create(
            title='Recycling Workshop',
            location='Forum',
            date=tomorrow.date(),
            time=tomorrow.time(),
            description='Learn proper recycling techniques'
        )
        
        next_week = timezone.now() + timedelta(days=7)
        self.event2 = Event.objects.create(
            title='Energy Conservation Talk',
            location='Harrison Building',
            date=next_week.date(),
            time=next_week.time(),
            description='Tips for conserving energy at home and work'
        )
        
        # Create a past event
        yesterday = timezone.now() - timedelta(days=1)
        self.past_event = Event.objects.create(
            title='Past Event',
            location='Old Building',
            date=yesterday.date(),
            time=yesterday.time(),
            description='This event has already happened'
        )
    
    def test_home_view_shows_only_future_events(self):
        """Test that only future events appear on the home page."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        
        # Check that future events are in the context
        self.assertIn('events', response.context)
        events = response.context['events']
        
        # Verify only future events are included
        self.assertIn(self.event1, events)
        self.assertIn(self.event2, events)
        self.assertNotIn(self.past_event, events)
        
        # Check that event titles appear on the page
        self.assertContains(response, 'Recycling Workshop')
        self.assertContains(response, 'Energy Conservation Talk')
        self.assertNotContains(response, 'Past Event')
    
    def test_events_section_displays_correctly(self):
        """Test that the events section has the expected structure."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        
        # Check for events container
        self.assertContains(response, '<div class="events-container">')
        self.assertContains(response, 'Upcoming Events')
        
        # Check for event details
        self.assertContains(response, 'Forum')  # Location of event1
        self.assertContains(response, 'Harrison Building')  # Location of event2
    
    def test_events_ordered_by_date(self):
        """Test that events are displayed in chronological order."""
        # Create another event with a date between the two existing future events
        in_three_days = timezone.now() + timedelta(days=3)
        middle_event = Event.objects.create(
            title='Mid-Week Event',
            location='Library',
            date=in_three_days.date(),
            time=in_three_days.time(),
            description='This should appear second in the list'
        )
        
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        
        events = list(response.context['events'])
        # Verify events are in chronological order
        self.assertEqual(events[0], self.event1)  # Tomorrow
        self.assertEqual(events[1], middle_event)  # In 3 days
        self.assertEqual(events[2], self.event2)  # In 7 days
    
    def test_event_with_subscription_displays_correctly(self):
        """Test that subscription information is displayed when available."""
        # Create an event with subscription information
        tomorrow = timezone.now() + timedelta(days=2)
        subscription_event = Event.objects.create(
            title='Subscription Event',
            location='Forum',
            date=tomorrow.date(),
            time=tomorrow.time(),
            description='An event requiring subscription',
            subscription='Email sustainability@example.com to join'
        )
        
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        
        # Check that subscription information appears on the page
        self.assertContains(response, 'Email sustainability@example.com to join')
        self.assertContains(response, 'How to join:')
    
    def test_no_events_message(self):
        """Test that a message is displayed when there are no events."""
        # Delete all events
        Event.objects.all().delete()
        
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        
        # Check for "no events" message
        self.assertContains(response, 'There are no events to display')
    
    def test_max_events_display_limit(self):
        """Test that only a limited number of events are displayed."""
        # Create 10 more future events
        for i in range(10):
            days_ahead = i + 10  # Start 10 days from now
            future_date = timezone.now() + timedelta(days=days_ahead)
            Event.objects.create(
                title=f'Future Event {i}',
                location='Campus',
                date=future_date.date(),
                time=future_date.time(),
                description=f'Event number {i}'
            )
        
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        
        # Count the number of events in the context
        self.assertEqual(len(response.context['events']), 5)  # Should be limited to 5
        
    def test_truncated_description(self):
        """Test that long descriptions are truncated in the template."""
        # Create an event with a long description
        long_desc = "This is a very long description that should be truncated in the template. " * 10
        tomorrow = timezone.now() + timedelta(days=1)
        event = Event.objects.create(
            title='Long Description Event',
            location='Forum',
            date=tomorrow.date(),
            time=tomorrow.time(),
            description=long_desc
        )
        
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        
        # The full description should not appear in the template
        self.assertNotContains(response, long_desc)
        
        # Instead of checking for the exact truncated content, check for 
        # the beginning of the description and the ellipsis character
        truncated_start = long_desc[:100]  # Check for a shorter portion to be safe
        self.assertContains(response, truncated_start)
        # Check that there's an ellipsis indicating truncation
        self.assertContains(response, "…")  # Unicode ellipsis character
