# Authors: Michael Porter and Nitzan Lahav

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages

class AuthenticationTests(TestCase):

    def setUp(self):
        """Set up a test user for login and sign-up tests."""
        self.username = 'testuser'
        self.password = 'password123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.save()

    def test_signup(self):
        """Test that a user can sign up successfully."""
        data = {
            'username': 'uniqueusername',
            'email': 'testuser@exeter.ac.uk',
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123',
        }
        response = self.client.post(reverse('signup'), data)

        # Check that the response status code is 302 (redirect after signup)
        self.assertEqual(response.status_code, 302)

        # Check that the redirect is to the login page
        self.assertRedirects(response, reverse('login'))

    def test_signup_without_exeter_email(self):
        """Test that a user cannot sign up without an @exeter.ac.uk email."""
        data = {
            'username': 'uniqueusername',
            'email': 'testuser@gmail.com',  # Invalid email (not @exeter.ac.uk)
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123',
        }
        response = self.client.post(reverse('signup'), data)

        # Check that the form is re-rendered (status code 200) after failed signup
        self.assertEqual(response.status_code, 200)
        
        # Check if the response contains the email validation error message
        self.assertContains(response, "Only @exeter.ac.uk emails are allowed.")

    def test_login(self):
        """Test that a user can log in successfully."""
        url = reverse('login')  # Replace with your actual login URL name
        response = self.client.post(url, {
            'username': self.username,
            'password': self.password,
        })

        # Check if login is successful and user is redirected to the home page
        self.assertEqual(response.status_code, 302)  # Expect redirect after successful login
        self.assertRedirects(response, reverse('home'))  # Replace with your home page URL name

    def test_login_with_invalid_credentials(self):
        """Test that logging in with invalid credentials does not work."""
        url = reverse('login')  # Replace with your actual login URL name
        response = self.client.post(url, {
            'username': 'nonexistentuser',  # Invalid username
            'password': 'wrongpassword',    # Invalid password
        })

        # Check that login fails and the page reloads with an error (status code 200)
        self.assertEqual(response.status_code, 200)
        
        # Check if the response contains an error message for invalid login
        self.assertContains(response, "Please enter a correct username and password.")

    def test_logout(self):
        """Test that a user can log out successfully."""
        self.client.login(username=self.username, password=self.password)
        url = reverse('logout')  # Replace with your actual logout URL name
        response = self.client.get(url)

        # Check if user is logged out and redirected to the login page
        self.assertEqual(response.status_code, 302)  # Expect redirect after logout
        self.assertRedirects(response, reverse('login'))  # Replace with your login page URL name

    def test_terms_and_conditions_redirect(self):
        """Test that the terms and conditions button redirects to the privacy policy page."""
        response = self.client.get(reverse('login'))  # Adjust if needed for the correct page

        # Ensure the page contains the privacy policy link
        self.assertContains(response, 'href="/privacy-policy"')
