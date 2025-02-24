# Authors: Michael Porter and Nitzan Lahav

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Must be an @exeter.ac.uk email address.")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith("@exeter.ac.uk"):
            raise ValidationError("Only @exeter.ac.uk emails are allowed.")
        return email

