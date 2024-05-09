from django import forms
from django.contrib.auth.models import User
from .models import Referral

class RegistrationForm(forms.ModelForm):

    ref_code = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class BuyThingForm(forms.Form):
    
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError('Сумма должна быть положительной')
        return amount