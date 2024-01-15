from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import VeterinarianUser

class VeterinarianUserCreationForm(UserCreationForm):
    class Meta:
        model = VeterinarianUser
        fields = ['username', 'email'] 