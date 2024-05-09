from django import forms
from django.contrib.auth.models import User
from .models import Referral

class RegistrationForm(forms.ModelForm):

    ref_code = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

