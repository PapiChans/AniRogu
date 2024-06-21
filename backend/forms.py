from django import forms
from backend.models import User
from django.core.exceptions import ValidationError

class SignupForm(forms.ModelForm): 
    password = forms.CharField(widget=forms.PasswordInput)
    cnfm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['profile_name', 'username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        cnfm_password = cleaned_data.get('cnfm_password')

        if password and cnfm_password and password != cnfm_password:
            raise ValidationError("Passwords do not match. Please enter matching passwords.")
        
        if password and len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        return cleaned_data
    
class LoginForm(forms.Form):
    username = forms.EmailField(label='Email address', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email Address'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Your Password', 'minlength': '8', 'maxlength': '20'}))

    def clean(self):
        cleaned_data = super().clean()
        # You can perform additional validation here if needed
        return cleaned_data