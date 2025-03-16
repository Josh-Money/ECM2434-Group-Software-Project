from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
import os
from django.conf import settings

class ContactViewTests(TestCase):
    """Tests for the contact page"""
    
    def setUp(self):
        # Set up test client
        self.client = Client()
        
        # Make a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
    
    def test_contact_view_get(self):
        """Check if contact page loads"""
        # Log in
        self.client.login(username='testuser', password='testpassword')
        
        # Get page
        response = self.client.get(reverse('contact'))
        
        # Should be 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Check template
        self.assertTemplateUsed(response, 'contact/contact.html')
    
    def test_contact_view_unauthenticated(self):
        """Check if logged out users get redirected"""
        response = self.client.get(reverse('contact'))
        
        # Should redirect (302)
        self.assertEqual(response.status_code, 302)
        
    def test_contact_page_contains_form(self):
        """Check if form is on the page"""
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.get(reverse('contact'))
        
        # Check form elements
        self.assertContains(response, '<form id="contact-form"')
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="message"')
        self.assertContains(response, 'type="submit"')

    def test_csrf_token_present(self):
        """Check if CSRF token is there"""
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.get(reverse('contact'))
        
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    def test_contact_js_loaded(self):
        """Check if JS files are loaded"""
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.get(reverse('contact'))
        
        self.assertContains(response, 'contact/js/contact.js')
        self.assertContains(response, 'email.min.js')
    
    def test_page_title(self):
        """Check page title"""
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.get(reverse('contact'))
        
        self.assertContains(response, '<title>Contact Us</title>')
    
    def test_heading_present(self):
        """Check if heading is there"""
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.get(reverse('contact'))
        
        self.assertContains(response, '<h1 class="title">Contact Us</h1>')
    
    def test_alternative_contact_info_present(self):
        """Check if email info is shown"""
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.get(reverse('contact'))
        
        self.assertContains(response, 'Alternatively, you can email us here:')
        self.assertContains(response, 'syntaxsquad2025@gmail.com')


class ContactFormValidationTests(TestCase):
    """Form validation tests"""
    
    def setUp(self):
        self.client = Client()
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.client.login(username='testuser', password='testpassword')
    
    def test_form_has_required_fields(self):
        """Check if fields are required"""
        response = self.client.get(reverse('contact'))
        
        self.assertContains(response, 'name="name" class="form-control" required')
        self.assertContains(response, 'name="email" class="form-control" required')
        self.assertContains(response, 'name="message" class="form-control" rows="5" required')
    
    def test_email_field_has_email_type(self):
        """Check if email field has right type"""
        response = self.client.get(reverse('contact'))
        
        self.assertContains(response, 'type="email"')
    
    def test_form_has_submit_button(self):
        """Check if submit button exists"""
        response = self.client.get(reverse('contact'))
        
        self.assertContains(response, '<button id="submit-btn" type="submit"')
        self.assertContains(response, 'Send Message</button>')
    
    def test_status_message_div_present(self):
        """Check if status message div exists"""
        response = self.client.get(reverse('contact'))
        
        self.assertContains(response, '<div id="status-message" class="mt-3 text-center" style="display: none;"></div>')


class ContactCssTests(TestCase):
    """CSS tests"""
    
    def setUp(self):
        self.client = Client()
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.client.login(username='testuser', password='testpassword')
    
    def test_css_loaded(self):
        """Check if CSS is loaded"""
        response = self.client.get(reverse('contact'))
        
        self.assertContains(response, 'contact/css/contact-styles.css')
    
    def test_template_extends_base(self):
        """Check if template extends base"""
        template_path = os.path.join(settings.BASE_DIR, 'contact', 'templates', 'contact', 'contact.html')
        
        # Make sure file exists
        self.assertTrue(os.path.exists(template_path), f"Template file not found at {template_path}")
        
        # Read file
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        self.assertIn("{% extends 'base.html' %}", template_content)
