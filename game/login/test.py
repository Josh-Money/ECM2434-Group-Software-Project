# Authors: Michael Porter and Nitzan Lahav

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages

class AuthenticationTests(TestCase):

    def setUp(self):
        """Make a test user for login tests."""
        self.username = 'testuser'
        self.password = 'password123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.save()

    def test_signup(self):
        """Check if signup form renders correctly."""
        data = {
            'username': 'uniqueusername',
            'email': 'testuser@exeter.ac.uk',
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123',
        }
        response = self.client.post(reverse('signup'), data)

        # The form should render (not redirect) because of the privacy policy checkbox
        self.assertEqual(response.status_code, 200)
        
        # Check that the form contains the username we tried to use
        self.assertContains(response, 'uniqueusername')

    def test_signup_password_mismatch(self):
        """Check if signup fails when passwords don't match."""
        data = {
            'username': 'uniqueusername',
            'email': 'testuser@exeter.ac.uk',
            'password1': 'StrongPassword123',
            'password2': 'DifferentPassword123',  # Different password
        }
        response = self.client.post(reverse('signup'), data)
        
        # Should stay on signup page
        self.assertEqual(response.status_code, 200)
        
        # Should show error message with special unicode apostrophe
        self.assertContains(response, "The two password fields didn")
        
        # User shouldn't be created
        self.assertFalse(User.objects.filter(username='uniqueusername').exists())

    def test_signup_without_exeter_email(self):
        """Check if non-exeter emails get rejected."""
        data = {
            'username': 'uniqueusername',
            'email': 'testuser@gmail.com',  # Not an exeter email
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123',
        }
        response = self.client.post(reverse('signup'), data)

        # Should stay on the same page
        self.assertEqual(response.status_code, 200)
        
        # Should show error message
        self.assertContains(response, "Only @exeter.ac.uk emails are allowed.")

    def test_login(self):
        """Check if login works."""
        url = reverse('login')
        response = self.client.post(url, {
            'username': self.username,
            'password': self.password,
        })

        # Should redirect after login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_login_with_invalid_credentials(self):
        """Check if wrong login details get rejected."""
        url = reverse('login')
        response = self.client.post(url, {
            'username': 'nonexistentuser',  # Wrong username
            'password': 'wrongpassword',    # Wrong password
        })

        # Should stay on login page
        self.assertEqual(response.status_code, 200)
        
        # Should show error
        self.assertContains(response, "Please enter a correct username and password.")

    def test_logout(self):
        """Check if logout works."""
        self.client.login(username=self.username, password=self.password)
        url = reverse('logout')
        response = self.client.get(url)

        # Should redirect after logout
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_terms_and_conditions_redirect(self):
        """Check if T&C link goes to privacy policy."""
        response = self.client.get(reverse('login'))

        # Should have privacy policy link
        self.assertContains(response, 'href="/privacy-policy"')
